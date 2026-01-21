class BloodRequestResponse:

    @staticmethod
    def short_detail(instance):
        return {
            'id': instance.id,
            'status': instance.status,
            'hospital': instance.hospital,
            'blood_type': instance.blood_type,
            'location': instance.location,
            'quantity': instance.quantity,
        }

    @staticmethod
    def detail(instance):
        return {
            'id': instance.id,
            'status': instance.status,
            'hospital': instance.hospital,
            'blood_type': instance.blood_type,
            'location': instance.location,
            'note': instance.note,
            'reason': instance.reason,
            'quantity': instance.quantity,
            'created_at': instance.created_at,
            'created_by': instance.created_by,
            'updated_at': instance.updated_at,
            'ended_at': instance.ended_at,
        }

    @staticmethod
    def detail_status(instance):
        return {
            'id': instance.id,
            'status': instance.status,
        }

    @staticmethod
    def list(instances):
        return [
            BloodRequestResponse.short_detail(instance)
            for instance in instances
        ]