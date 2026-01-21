from api.models import BloodRequest
from django.db.models import Q

class BloodRequestRepository:
    @staticmethod
    def get_all_other_request(user_id):
        # all request from others
        return (
            BloodRequest.objects
            .filter(deleted_at__isnull=True)
            .exclude(Q(created_by=user_id) | Q(status__in=['cancelled', 'ended']))
        )

    @staticmethod
    def get_all_self_request(user_id):
        # all request from own self was created
        return (
            BloodRequest.objects
            .filter(created_by=user_id, deleted_at__isnull=True)
            .exclude(status__in=['cancelled', 'ended'])
        )

    @staticmethod
    def get_one(pk):
        # detail on one request which is from other or own self
        return (
            BloodRequest.objects
            .filter(pk=pk, deleted_at__isnull=True)
            .exclude(status__in=['cancelled'])
            .first()
        )

    @staticmethod
    def get_one_self_by_status(user_id, pk, status='pending'):
        return (
            BloodRequest.objects
            .filter(pk=pk, deleted_at__isnull=True, status=status, created_by=user_id)
            .first()
        )

    @staticmethod
    def get_blood_pending(user_id, pk, status='pending'):
        return (
            BloodRequest.objects
            .filter(pk=pk, deleted_at__isnull=True, status=status)
            .exclude(created_by=user_id)
            .first()
        )