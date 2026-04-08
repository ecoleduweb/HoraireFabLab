from rest_framework import serializers
from api.models import Slot
import nh3


def sanitize(value: str) -> str:
    return nh3.clean(value, tags=set())


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ["id", "plage", "start_at", "end_at", "client_fname", "client_lname", "client_email", "client_phone", "item", "item_description", "liability_accepted", "is_canceled", "updated_at", "created_at"]
        read_only_fields = ["id", "created_at", "updated_at", "is_canceled"]

    def validate_client_fname(self, value):
        return sanitize(value)

    def validate_client_lname(self, value):
        return sanitize(value)

    def validate_client_email(self, value):
        return sanitize(value)

    def validate_client_phone(self, value):
        return sanitize(value)

    def validate_item(self, value):
        return sanitize(value)

    def validate_item_description(self, value):
        return sanitize(value)