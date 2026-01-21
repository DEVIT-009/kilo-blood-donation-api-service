from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from api.controllers.dto.responses.blood_request_response import BloodRequestResponse
from api.services.blood_request_service import BloodRequestService
from api.utilities.metadata_handler.request_header_utillity import metadata_handler, Metadata
from api.utilities.responseutils.response_handler import ResponseHandler

class BloodView(ViewSet):

    @metadata_handler(required_user_id=True)
    def list_request(self, request: Request, metadata: Metadata, *args, **kwargs):
        data = BloodRequestService.list_all_request(metadata=metadata)
        blood_request = BloodRequestResponse.list(data)
        return ResponseHandler.success(
            data=blood_request,
            message="RETRIEVE SUCCESSFULLY"
        )

    @metadata_handler(required_user_id=True)
    def list_own_request(self, request: Request, metadata: Metadata, *args, **kwargs):
        data = BloodRequestService.list_all_own_request(metadata=metadata)
        blood_request = BloodRequestResponse.list(data)
        return ResponseHandler.success(
            data=blood_request,
            message="RETRIEVE SUCCESSFULLY"
        )

    @metadata_handler(required_user_id=True)
    def detail_request(self, request: Request, metadata: Metadata, pk, *args, **kwargs):
        data = BloodRequestService.detail(metadata=metadata, pk=pk)
        blood_request = BloodRequestResponse.detail(data)
        return ResponseHandler.success(
            data=blood_request,
            message="RETRIEVE SUCCESSFULLY"
        )

    @metadata_handler(required_user_id=True)
    def create(self, request: Request, metadata: Metadata, *args, **kwargs):
        data, error = BloodRequestService.create(data=request.data, metadata=metadata)

        if error:
            return ResponseHandler.bad_request(data={"error": error})

        blood_request = BloodRequestResponse.detail(data)
        return ResponseHandler.created(
            data=blood_request,
        )

    @metadata_handler(required_user_id=True)
    def update(self, request: Request, metadata: Metadata, pk,  *args, **kwargs):
        data, error = BloodRequestService.update(data=request.data, metadata=metadata, pk=pk)

        if error:
            return ResponseHandler.bad_request(data={"error": error})

        blood_request = BloodRequestResponse.detail(data)
        return ResponseHandler.updated(
            data=blood_request,
        )

    @metadata_handler(required_user_id=True)
    def destroy(self, request: Request, metadata: Metadata, pk, *args, **kwargs):
        BloodRequestService.delete(metadata=metadata, pk=pk)
        return ResponseHandler.deleted()

    @metadata_handler(required_user_id=True)
    def ended_request(self, request: Request, metadata: Metadata, pk, *args, **kwargs):
        data, error = BloodRequestService.ended(metadata=metadata, pk=pk)
        if error:
            return ResponseHandler.bad_request(data={"error": error})

        blood_request = BloodRequestResponse.detail(data)
        return ResponseHandler.updated(
            data=blood_request,
            message="ENDED SUCCESSFULLY"
        )

    @metadata_handler(required_user_id=True)
    def cancelled_request(self, request: Request, metadata: Metadata, pk, *args, **kwargs):
        data, error = BloodRequestService.cancelled(metadata=metadata, pk=pk)
        if error:
            return ResponseHandler.bad_request(data={"error": error})

        blood_request = BloodRequestResponse.detail_status(data)
        return ResponseHandler.updated(
            data=blood_request,
            message="CANCELLED SUCCESSFULLY"
        )