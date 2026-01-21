from django.urls import path

from api.controllers.views.blood_request_view import BloodView

urlpatterns = [
    path('blood-request', BloodView.as_view({
        'post': 'create'
    }), name='blood-create'),
    path('blood-request/blood-request', BloodView.as_view({
        'get': 'list_request'
    }), name='blood-list-request'),
    path('blood-request/own-request', BloodView.as_view({
        'get': 'list_own_request'
    }), name='blood-list-own-request'),
    path('blood-request/<int:pk>', BloodView.as_view({
        'get': 'detail_request',
        'put': 'update',
        'delete': 'destroy'
    }), name='blood-detail-update-delete'),
    path('blood-request/<int:pk>/ended', BloodView.as_view({
        'patch': 'ended_request'
    }), name='blood-ended'),
    path('blood-request/<int:pk>/cancelled', BloodView.as_view({
        'patch': 'cancelled_request'
    }), name='blood-ended'),
]