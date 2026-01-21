import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone

from .auth_exception import AuthException  # adjust import path
from ..models import User


class JwtUtil:

    SECRET_KEY = getattr(settings, "JWT_SECRET_KEY")
    EXPIRATION_MS = getattr(settings, "JWT_EXPIRATION_MS", 3_600_000)  # default 1 hour
    REFRESH_EXPIRATION_MS = getattr(settings, "JWT_REFRESH_EXPIRATION_MS", 7)  # default 7 days

    @classmethod
    def generate_tokens(cls, user):
        now = datetime.now(timezone.utc)

        access_payload = {
            "sub": user.phone_number,
            "iat": now,
            "exp": now + timedelta(milliseconds=cls.EXPIRATION_MS),  # short life
            "type": "access"
        }

        refresh_payload = {
            "sub": user.phone_number,
            "iat": now,
            "exp": now + timedelta(milliseconds=cls.REFRESH_EXPIRATION_MS),    # long life
            "type": "refresh"
        }

        access_token = jwt.encode(access_payload, cls.SECRET_KEY, algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, cls.SECRET_KEY, algorithm="HS256")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    @classmethod
    def extract_phone_number(cls, token):
        """
        Extract id (subject) from JWT token.
        """
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=["HS256"])
            return payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise AuthException.unauthorized()
        except jwt.InvalidTokenError:
            raise AuthException.unauthorized()

    @classmethod
    def is_token_expired(cls, token):
        """
        Return True if the token is expired.
        """
        try:
            jwt.decode(token, cls.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True})
            return False
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            raise AuthException.unauthorized()

    @classmethod
    def validate_token(cls, token, user):
        """
        Validate token: check username matches and token is not expired.
        """
        phone_number = cls.extract_phone_number(token)
        return phone_number == user.phone_number and not cls.is_token_expired(token)

    @classmethod
    def validate_and_get_user(cls, token):
        """
        Validate token and return corresponding User instance.
        Raises AuthException if invalid or user does not exist.
        """
        phone_number = cls.extract_phone_number(token)
        try:
            user = User.objects.get(phone_number=phone_number)
            if not cls.validate_token(token, user):
                raise AuthException.unauthorized()
            return user
        except User.DoesNotExist:
            raise AuthException.unauthorized()