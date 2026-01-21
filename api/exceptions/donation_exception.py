from rest_framework import status

from api.utilities.exceptionalhandler.base_api_exception import BaseAPIException

class DonationException(BaseAPIException):
    @classmethod
    def not_found(cls):
        return cls.create(status.HTTP_404_NOT_FOUND, "DONATION_NOT_FOUND")

    @classmethod
    def already_exists(cls, message="DONATION_ALREADY_EXISTS"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message=message)

    @classmethod
    def bad_request(cls, message="BAD_REQUEST"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message=message)
