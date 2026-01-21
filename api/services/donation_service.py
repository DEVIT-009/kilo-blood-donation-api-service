from django.db import transaction
from django.utils import timezone

from api.controllers.dto.serializers.donation_serializer import DonationSerializer
from api.exceptions.blood_request_exception import BloodRequestException
from api.exceptions.donation_exception import DonationException
from api.repositories.blood_request_repository import BloodRequestRepository
from api.repositories.donation_repository import DonationRepository
from api.utilities.metadata_handler.request_header_utillity import Metadata

class DonationService:

    @staticmethod
    def detail(pk, user_id):
        donation = DonationRepository.get_donation_by_id(user_id=user_id, pk=pk)
        if not donation:
            raise DonationException.not_found()
        return donation

    @staticmethod
    def list_self_offered(metadata: Metadata):
        return DonationRepository.get_all_self_offered(metadata.user_id)

    @staticmethod
    @transaction.atomic()
    def offered(metadata: Metadata, pk):
        blood_request_pending = BloodRequestRepository.get_blood_pending(user_id=metadata.user_id, pk=pk)
        if not blood_request_pending:
            raise BloodRequestException.cannot_donate_own_request()

        donation_payload = {
            'status': 'offered',
            'request_id': pk,
            'donor_id': metadata.user_id,
        }
        if blood_request_pending:
            blood_request_pending.status = 'active'
            blood_request_pending.save(update_fields=['status'])
        serialize = DonationSerializer(data=donation_payload)
        if serialize.is_valid():
            donation_instance = serialize.save()
            return donation_instance, None
        return None, serialize.errors

    @classmethod
    @transaction.atomic()
    def cancelled_by_donor(cls, user_id, pk):
        donation = DonationRepository.get_one_self_offered(user_id=user_id, pk=pk)
        if not donation:
            raise DonationException.bad_request(message='CANNOT_CANCELLED_BLOOD_ALREADY_ACCEPTED')

        serialize = DonationSerializer(
            instance=donation,
            data={'status': 'cancelled'},
            partial=True
        )
        if serialize.is_valid():
            donation_instance = serialize.save()
            return donation_instance, None
        return None, serialize.errors

    @staticmethod
    @transaction.atomic()
    def accepted_donation(user_id, pk):
        donation = DonationRepository.get_offered_for_accepted(user_id=user_id, donation_id=pk)
        if not donation:
            raise DonationException.not_found()
        donation.status = 'accepted'
        donation.save(update_fields=['status'])
        return donation

    @staticmethod
    @transaction.atomic()
    def completed_donation(user_id, pk):
        donation = DonationRepository.get_accepted(user_id=user_id, donation_id=pk)
        if not donation:
            raise DonationException.not_found()
        donation.status = 'completed'
        donation.completed_at = timezone.now()

        blood_request = BloodRequestRepository.get_request_by_id(user_id=user_id, request_id=donation.request_id)
        if not blood_request:
            raise BloodRequestException.not_found()
        blood_request.status = 'ended'
        blood_request.ended_at = timezone.now()

        donation.save(update_fields=['status', 'completed_at'])
        blood_request.save(update_fields=['status', 'ended_at'])
        return donation

    @staticmethod
    @transaction.atomic()
    def declined_donation(user_id, pk):
        donation = DonationRepository.get_accepted(user_id=user_id, donation_id=pk)
        if not donation:
            raise DonationException.not_found()
        donation.status = 'declined'

        donation.save(update_fields=['status'])
        return donation