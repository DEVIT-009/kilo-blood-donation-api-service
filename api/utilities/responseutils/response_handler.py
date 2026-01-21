from rest_framework import status
from rest_framework.response import Response

class ResponseHandler:

    @staticmethod
    def success(data, message="OPERATION SUCCESSFULLY"):
        return Response({
            "status": "SUCCESS",
            "message": message,
            "data": data
        }, status=status.HTTP_200_OK)

    @staticmethod
    def created(data, message="CREATED SUCCESSFULLY"):
        return Response({
            "status": "SUCCESS",
            "message": message,
            "data": data
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def updated(data, message="UPDATED SUCCESSFULLY"):
        return Response({
            "status": "SUCCESS",
            "message": message,
            "data": data
        }, status=status.HTTP_200_OK)

    @staticmethod
    def deleted(message=None, data=None):
        return Response({
            "message": message or "DELETED SUCCESSFULLY",
            "data": data
        }, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def bad_request(message=None, data=None):
        return Response({
            "message": message or "BAD REQUEST",
            "data": data
        }, status=status.HTTP_400_BAD_REQUEST)
