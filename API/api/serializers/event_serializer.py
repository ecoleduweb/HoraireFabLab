from rest_framework import serializers
from api.models import Event
from api.utils.sanitize import sanitize


class EventSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    event_date = serializers.DateField(required=True)

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = ["id", "name", "event_date", "created_at"]
        read_only_fields = ["id", "created_at"]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        if 'name' in ret and isinstance(ret['name'], str):
            ret['name'] = sanitize(ret['name'])

        return ret