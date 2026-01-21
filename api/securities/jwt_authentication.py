from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from .jwt_util import JwtUtil
from .auth_exception import AuthException


class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # Get Head section Authorization which is has
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise AuthException.unauthorized()
        except ValueError:
            raise AuthException.unauthorized()

        phone_number = JwtUtil.extract_phone_number(token)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise AuthException.unauthorized()

        if not JwtUtil.validate_token(token, user):
            raise AuthException.unauthorized()

        return user, None