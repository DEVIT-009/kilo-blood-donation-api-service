from rest_framework import status

from api.utilities.exceptionalhandler.base_api_exception import BaseAPIException


class UserException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "USER NOT FOUND")

    @classmethod
    def already_exists(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, "USER ALREADY EXISTS")

    @classmethod
    def bad_request(cls, message="BAD REQUEST"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message=message)
