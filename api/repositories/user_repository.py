from api.models import User

class UserRepository():
    @staticmethod
    def exists_by_phone_number(phone_number, exclude_id=None):
        query = User.objects.filter(
            phone_number=phone_number,
            enabled=True
        )

        if exclude_id is not None:
            query = query.exclude(id=exclude_id)

        return query.exists()

    @staticmethod
    def get_by_phone_number(phone_number):
        return User.objects.filter(
            phone_number=phone_number,
            enabled=True
        ).first()