from django.http import JsonResponse
from api.securities.jwt_util import JwtUtil
from api.securities.auth_exception import AuthException
import jwt

class AdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/v1/admin/**"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return AuthException.forbidden()

            token = auth_header[7:]
            try:
                user = JwtUtil.validate_and_get_user(token)
                if not user.is_superuser:
                    return AuthException.forbidden()
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, AuthException):
                return AuthException.forbidden()

        return self.get_response(request)