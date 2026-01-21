from django.db import transaction
from django.utils import timezone

from rest_framework.viewsets import ViewSet
from django.contrib.auth import authenticate

from .auth_exception import AuthException
from .jwt_util import JwtUtil
from api.repositories.user_repository import UserRepository
from .user_serializer import UserRegisterSerializer, UserLoginSerializer
from ..utilities.responseutils.response_handler import ResponseHandler

class AuthView(ViewSet):

    @staticmethod
    def _validate_phone_number(phone_number):
        if UserRepository.exists_by_phone_number(phone_number=phone_number):
            raise AuthException.bad_request(message="PHONE NUMBER ALREADY TAKEN")

    @staticmethod
    def _validate_password(password, confirm_password):
        if len(password) < 8:
            raise AuthException.bad_request(message="PASSWORD TOO SHORT")
        if confirm_password != password:
            raise AuthException.bad_request("PASSWORD MISMATCH")

    def login_admin(self, request, *args, **kwargs):
        data = request.data
        phone_number = data.get("phone_number")
        password = data.get("password")

        if not phone_number or not password:
            raise ResponseHandler.bad_request(message="Phone number and password are required.")

        user = UserRepository.get_by_phone_number(phone_number)
        if not user or not user.check_password(password):
            raise AuthException.unauthorized(message="Invalid phone number or password.")

        if not user.is_active:
            raise AuthException.unauthorized(message="Account is inactive.")

        # Check if user is staff or superuser
        if not user.is_staff:
            raise AuthException.unauthorized(message="You do not have admin access.")

        # Update login time
        user.last_logged_in_at = timezone.now()
        user.save(update_fields=["last_logged_in_at"])

        # Generate tokens
        token_value = JwtUtil.generate_tokens(user)

        return ResponseHandler.success(
            message="login successfully.",
            data={
                "access_token": token_value['access_token'],
                "refresh_token": token_value['refresh_token'],
            },
        )

    def login_user(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if not serializer.is_valid():
            return ResponseHandler.bad_request(
                message="Invalid input", data=serializer.errors
            )

        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise AuthException.unauthorized(message="INVALID PHONE NUMBER OR PASSWORD")
        if not user.is_active:
            raise AuthException.unauthorized(message="Account is inactive.")

        # Update login time
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # Generate tokens
        token_value = JwtUtil.generate_tokens(user)

        return ResponseHandler.success(
            message="Login successfully.",
            data={
                "access_token": token_value['access_token'],
                "refresh_token": token_value['refresh_token'],
            },
        )

    def register_user(self, request, *args, **kwargs):
        data = request.data
        phone_number = data.get("phone_number")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        AuthView._validate_password(password=password, confirm_password=confirm_password)
        AuthView._validate_phone_number(phone_number=phone_number)

        with transaction.atomic():
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                token_value = JwtUtil.generate_tokens(user)
                return ResponseHandler.success(
                    message= "Register successfully.",
                    data={
                        "access_token": token_value['access_token'],
                        "refresh_token": token_value['refresh_token'],
                    },
                )
            return ResponseHandler.bad_request(
                message="Invalid input",
                data=serializer.errors
            )

