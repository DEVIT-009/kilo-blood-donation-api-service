from api.controllers.dto.responses.blood_request_response import BloodRequestResponse


class DonationResponse:

    @staticmethod
    def _format_request(request):
        if not request:
            return None
        return BloodRequestResponse.short_detail(request)

    @classmethod
    def short_detail(cls, instance):
        return {
            'id': instance.id,
            'status': instance.status,
            'donor_id': instance.donor_id,
            'completed_at': instance.completed_at,
            'request': cls._format_request(instance.request),
        }

    @classmethod
    def detail(cls, instance):
        return {
            'id': instance.id,
            'status': instance.status,
            'donor_id': instance.donor_id,
            'created_at': instance.created_at,
            'completed_at': instance.completed_at,
            'request': cls._format_request(instance.request),
        }

    @staticmethod
    def detail_status(instance):
        return {
            'id': instance.id,
            'status': instance.status,
        }

    @classmethod
    def list(cls, instances):
        return [
            cls.short_detail(post)
            for post in instances
        ]