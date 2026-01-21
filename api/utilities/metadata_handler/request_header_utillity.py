# api/utilities/metadata_handler/metadata.py
from functools import wraps
from rest_framework.request import Request

from api.securities.auth_exception import AuthException
from api.securities.jwt_util import JwtUtil


class Metadata:
    def __init__(self, user_id=None, merchant_id=None, app_id=None, merchant_app_id=None):
        self.user_id = user_id  # Will hold username from JWT
        self.merchant_id = merchant_id
        self.app_id = app_id
        self.merchant_app_id = merchant_app_id

def metadata_handler(required_user_id=True):
    """
    Decorator to inject Metadata into view methods.
    Extracts username from JWT and sets metadata.user_id.
    If required_user_id=True, JWT must be provided and valid.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(view, request: Request, *args, **kwargs):
            metadata = Metadata()

            auth_header = request.headers.get("Authorization")
            if required_user_id:
                if not auth_header or not auth_header.startswith("Bearer "):
                    raise AuthException.unauthorized()

                token = auth_header[7:]  # Remove "Bearer "
                try:
                    phone_number = JwtUtil.extract_phone_number(token)
                    metadata.user_id = phone_number
                except AuthException:
                    raise AuthException.unauthorized()

            return func(view, request, metadata, *args, **kwargs)
        return wrapper
    return decorator
