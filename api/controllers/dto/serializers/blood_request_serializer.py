from api.models import BloodRequest
from rest_framework import serializers

class BloodRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloodRequest
        fields = [
            'id', 'blood_type', 'hospital', 'location', 'note', 'status',
            'reason', 'quantity',
            'created_at', 'created_by', 'updated_at', 'deleted_at', 'ended_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'ended_at']