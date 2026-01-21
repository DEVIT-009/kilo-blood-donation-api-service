from api.models import Donation

class DonationRepository():
    @staticmethod
    def get_donation_by_id(user_id, pk):
        return (
            Donation.objects
            .filter(donor_id=user_id, pk=pk)
            .first()
        )

    @staticmethod
    def get_all_self_offered(user_id):
        # all donation from others
        return (
            Donation.objects
            .filter(completed_at__isnull=True, donor_id=user_id, status='offered')
        )
    @staticmethod
    def get_all_accepted(user_id):
        # all donation from others
        return (
            Donation.objects
            .filter(completed_at__isnull=True, donor_id=user_id, status='accepted')
        )

    @staticmethod
    def get_one_self_offered(user_id, pk):
        # all request from others
        return (
            Donation.objects
            .filter(completed_at__isnull=True, donor_id=user_id, status='offered', pk=pk)
            .first()
        )