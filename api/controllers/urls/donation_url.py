from django.urls import path

from api.controllers.views.donation_view import DonationView

urlpatterns = [
    path('donation/self-offered', DonationView.as_view({
        'get': 'list_self_offered'
    }), name='donation-list-offered'),
    path('donation/self-accepted', DonationView.as_view({
        'get': 'list_self_accepted'
    }), name='donation-list-self-accepted'),
    path('donation/got-accepted', DonationView.as_view({
        'get': 'list_got_accepted'
    }), name='donation-list-got-accepted'),
    path('donation/<int:pk>/offered', DonationView.as_view({
        'post': 'offered_request'
    }), name='donation-post-offered'),
    path('donation/<int:pk>/accepted', DonationView.as_view({
        'put': 'accepted_donation'
    }), name='donation-post-accepted'),
    path('donation/<int:pk>/cancelled', DonationView.as_view({
        'patch': 'cancelled_by_donor'
    }), name='donation-patch-cancelled-by-donor'),
    path('donation/<int:pk>/completed', DonationView.as_view({
        'put': 'completed_donation'
    }), name='donation-post-completed'),
    path('donation/<int:pk>/declined', DonationView.as_view({
        'put': 'declined_donation'
    }), name='donation-post-declined'),
]