from rest_framework import serializers

from api.models import Donation, BloodRequest


class DonationSerializer(serializers.ModelSerializer):
    request_id = serializers.PrimaryKeyRelatedField(
        queryset=BloodRequest.objects.all(),
        source='request',
        required=True,
        allow_null=False
    )

    class Meta:
        model = Donation
        fields = [
            'id', 'status', 'request_id', 'donor_id',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']