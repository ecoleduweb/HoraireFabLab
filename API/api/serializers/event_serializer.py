from rest_framework import serializers
from api.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "event_date", "created_at"]
        read_only_fields = ["id", "created_at"]