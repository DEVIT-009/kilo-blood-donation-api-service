from api.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Seed default users"

    def handle(self, *args, **options):
        users = [
            {"phone_number": "0967234500", "password": "Devit009", "is_superuser": True, "is_staff": True},
            {"phone_number": "0967234501", "password": "Devit009", "is_superuser": False, "is_staff": True},
            {"phone_number": "0967234502", "password": "Devit009", "is_superuser": False, "is_staff": False},
        ]

        for data in users:
            phone_number = data["phone_number"]

            if User.objects.filter(phone_number=phone_number).exists():
                self.stdout.write(self.style.WARNING(f"User '{phone_number}' already exists."))
                continue

            user = User.objects.create_user(
                phone_number=phone_number,
                password=data["password"],
                is_staff=data["is_staff"],
                is_superuser=data["is_superuser"],
                enabled=True,
            )

            self.stdout.write(self.style.SUCCESS(f"User '{phone_number}' created successfully!"))
