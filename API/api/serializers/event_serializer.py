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
        if 'eventDate' in data and 'event_date' not in data:
            data = data.copy()
            data['event_date'] = data.pop('eventDate')

        ret = super().to_internal_value(data)

        if 'name' in ret and isinstance(ret['name'], str):
            ret['name'] = sanitize(ret['name'])

        return ret

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['eventDate'] = ret.pop('event_date')
        ret['createdAt'] = ret.pop('created_at')
        return ret