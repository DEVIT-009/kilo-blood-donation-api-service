from django.db import models

from api.models import BloodRequest


class Donation(models.Model):
    STATUS_CHOICES = [
        ("offered", "Offered"),     # donor offered to donate
        ("accepted", "Accepted"),   # requester accepted donor
        ("declined", "Declined"),   # requester declined donor
        ("completed", "Completed"), # donation completed
        ("cancelled", "Cancelled"), # donor or requester cancelled
    ]

    request = models.ForeignKey(
        BloodRequest,
        on_delete=models.CASCADE,
        db_column='request_id',
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="offered")

    donor_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "donation"
        unique_together = ("request", "donor_id")

    def __str__(self):
        return f"Donation by {self.donor_id} for Request {self.request_id} ({self.status})"
