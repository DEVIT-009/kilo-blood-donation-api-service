from rest_framework import status

from api.utilities.exceptionalhandler.base_api_exception import BaseAPIException

class BloodRequestException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "REQUEST_NOT_FOUND")

    @classmethod
    def already_exists(cls, message="REQUEST_ALREADY_EXISTS"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message=message)

    @classmethod
    def bad_request(cls, message="BAD_REQUEST"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message=message)

    @classmethod
    def cannot_donate_own_request(cls):
        return cls.create(status.HTTP_400_BAD_REQUEST, message="CANNOT_DONATE_OWN_REQUEST")