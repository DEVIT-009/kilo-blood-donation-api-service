from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

from api.controllers.dto.responses.donation_response import DonationResponse
from api.services.donation_service import DonationService
from api.utilities.metadata_handler.request_header_utillity import metadata_handler, Metadata
from api.utilities.responseutils.response_handler import ResponseHandler

class DonationView(ViewSet):

    @metadata_handler(required_user_id=True)
    def list_self_offered(self, request: Request, metadata: Metadata, *args, **kwargs):
        data = DonationService.list_self_offered(metadata=metadata)
        blood_request = DonationResponse.list(data)
        return ResponseHandler.success(
            data=blood_request,
            message="RETRIEVE SUCCESSFULLY"
        )

    @metadata_handler(required_user_id=True)
    def offered_request(self, request: Request, metadata: Metadata, pk, *args, **kwargs):
        data, error = DonationService.offered(metadata=metadata, pk=pk)
        if error:
            return ResponseHandler.bad_request(data={"error": error})

        donation = DonationResponse.detail(data)
        return ResponseHandler.updated(
            data=donation,
            message="OFFERED SUCCESSFULLY"
        )

    @metadata_handler(required_user_id=True)
    def cancelled_by_donor(self, request: Request, metadata: Metadata, pk=None, *args, **kwargs):
        data, error = DonationService.cancelled_by_donor(user_id=metadata.user_id, pk=pk)
        if error:
            return ResponseHandler.bad_request(data={"error": error})

        donation = DonationResponse.detail(data)
        return ResponseHandler.created(
            data=donation,
            message="CANCELLED SUCCESSFULLY"
        )

    @metadata_handler(required_user_id=True)
    def accepted_donation(self, request: Request, metadata: Metadata, pk=None, *args, **kwargs):
        data = DonationService.accepted_donation(user_id=metadata.user_id, pk=pk)
        donation = DonationResponse.detail(data)
        return ResponseHandler.updated(
            data=donation,
            message="ACCEPTED DONATION SUCCESSFULLY"
        )

    @metadata_handler(required_user_id=True)
    def completed_donation(self, request: Request, metadata: Metadata, pk=None, *args, **kwargs):
        data = DonationService.completed_donation(user_id=metadata.user_id, pk=pk)
        donation = DonationResponse.detail(data)
        return ResponseHandler.updated(
            data=donation,
            message="COMPLETED DONATION SUCCESSFULLY"
        )

    @metadata_handler(required_user_id=True)
    def declined_donation(self, request: Request, metadata: Metadata, pk=None, *args, **kwargs):
        data = DonationService.declined_donation(user_id=metadata.user_id, pk=pk)
        donation = DonationResponse.detail(data)
        return ResponseHandler.updated(
            data=donation,
            message="COMPLETED DONATION SUCCESSFULLY"
        )