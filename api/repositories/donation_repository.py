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
    def list_self_offered(user_id):
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

    @staticmethod
    def get_offered_for_accepted(user_id, donation_id: int):
        return (
            Donation.objects
            .filter(
                id=donation_id,
                completed_at__isnull=True,
                request__created_by=user_id,
                status='offered',
            )
            .first()
        )

    @staticmethod
    def get_accepted(user_id, donation_id: int):
        return (
            Donation.objects
            .filter(
                id=donation_id,
                completed_at__isnull=True,
                request__created_by=user_id,
                status='accepted',
            )
            .first()
        )

    @staticmethod
    def list_self_accepted(user_id):
        return (
            Donation.objects
            .filter(
                completed_at__isnull=True,
                request__created_by=user_id,
                status='accepted',
            )
        )

    @staticmethod
    def list_got_accepted(user_id):
        return (
            Donation.objects
            .filter(
                completed_at__isnull=True,
                status='accepted',
                donor_id=user_id,
            )
        )