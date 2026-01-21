from rest_framework import status

from api.utilities.exceptionalhandler.base_api_exception import BaseAPIException


class AuthException(BaseAPIException):

    @classmethod
    def unauthorized(cls, message="Unauthorized"):
        return cls.create(
            status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code="AUTH_401"
        )

    @classmethod
    def forbidden(cls, message="Forbidden"):
        return cls.create(
            status.HTTP_403_FORBIDDEN,
            message=message,
            error_code="AUTH_403"
        )

    @classmethod
    def bad_request(cls, message="BAD_REQUEST"):
        return cls.create(
            status.HTTP_400_BAD_REQUEST,
            message=message,
            error_code="AUTH_400"
        )