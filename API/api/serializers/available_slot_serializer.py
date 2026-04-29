from rest_framework import serializers

class AvailableSlotSerializer(serializers.Serializer):
    plage_id = serializers.IntegerField()
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()