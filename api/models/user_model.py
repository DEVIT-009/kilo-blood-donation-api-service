from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("enabled", True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    username = None

    phone_number = models.CharField(max_length=20, unique=True)

    account_non_expired = models.BooleanField(default=True)
    account_non_locked = models.BooleanField(default=True)
    credentials_non_expired = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)
    status = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.phone_number