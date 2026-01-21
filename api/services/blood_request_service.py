from django.utils import timezone
from django.db import transaction

from api.controllers.dto.serializers.blood_request_serializer import BloodRequestSerializer
from api.exceptions.blood_request_exception import BloodRequestException
from api.repositories.blood_request_repository import BloodRequestRepository
from api.utilities.metadata_handler.request_header_utillity import Metadata

class BloodRequestService:
    @staticmethod
    def _build_payload(request_data, metadata: Metadata, data_db=None):
        payload = {
            'blood_type': request_data.get('blood_type') or getattr(data_db, 'blood_type', None),
            'hospital': request_data.get('hospital') or getattr(data_db, 'hospital', None),
            'location': request_data.get('location') or getattr(data_db, 'location', None),
            'note': request_data.get('note') or getattr(data_db, 'note', None),
            'reason': request_data.get('reason') or getattr(data_db, 'reason', None),
            'quantity': request_data.get('quantity') or getattr(data_db, 'quantity', 1),

            'created_by': metadata.user_id,
        }
        return payload

    @staticmethod
    def detail(metadata:Metadata, pk):
        data = BloodRequestRepository.get_one(pk=pk)
        if not data:
            raise BloodRequestException.not_found()
        return data

    @staticmethod
    def list_all_request(metadata: Metadata):
        return BloodRequestRepository.get_all_other_request(metadata.user_id)

    @staticmethod
    def list_all_own_request(metadata: Metadata):
        return BloodRequestRepository.get_all_self_request(metadata.user_id)

    @staticmethod
    def create(data, metadata: Metadata):
        payload = BloodRequestService._build_payload(request_data=data, metadata=metadata)
        with transaction.atomic():
            serialize = BloodRequestSerializer(data=payload)
            if serialize.is_valid():
                create_instance = serialize.save()
                return create_instance, None
            return None, serialize.errors

    @staticmethod
    def update(data, metadata: Metadata, pk):
        blood_request = BloodRequestRepository.get_one_self_by_status(user_id=metadata.user_id, pk=pk)

        if not blood_request:
            BloodRequestException.not_found()

        payload = BloodRequestService._build_payload(
            request_data=data,
            metadata=metadata,
            data_db=blood_request
        )
        with transaction.atomic():
            serialize = BloodRequestSerializer(instance=blood_request, data=payload, partial=True)
            if serialize.is_valid():
                update_instance = serialize.save()
                return update_instance, None
            return None, serialize.errors

    @staticmethod
    def delete(metadata: Metadata, pk):
        data = BloodRequestRepository.get_one_self_by_status(user_id=metadata.user_id, pk=pk)
        if not data:
            raise BloodRequestException.not_found()

        with transaction.atomic():
            data.deleted_at = timezone.now()
            data.save()

    @staticmethod
    def ended(metadata: Metadata, pk):
        blood_request = BloodRequestRepository.get_one_self_by_status(metadata.user_id, pk=pk, status='active')
        if not blood_request:
            raise BloodRequestException.not_found()

        payload = {
            "status": "ended",
            "ended_at": timezone.now(),
        }
        with transaction.atomic():
            serialize = BloodRequestSerializer(instance=blood_request, data=payload, partial=True)
            if serialize.is_valid():
                update_instance = serialize.save()
                return update_instance, None
            return None, serialize.errors

    @staticmethod
    def cancelled(metadata: Metadata, pk):
        blood_request = BloodRequestRepository.get_one_self_by_status(metadata.user_id, pk=pk)
        if not blood_request:
            raise BloodRequestException.not_found()

        payload = {"status": "cancelled"}
        with transaction.atomic():
            serialize = BloodRequestSerializer(instance=blood_request, data=payload, partial=True)
            if serialize.is_valid():
                update_instance = serialize.save()
                return update_instance, None
            return None, serialize.errors