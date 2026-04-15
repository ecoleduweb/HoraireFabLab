from rest_framework import serializers
from api.models import Slot, Plage
import nh3
from django.db import models


def sanitize(value: str) -> str:
    return nh3.clean(value, tags=set())

class SlotSerializer(serializers.ModelSerializer):
    plage = serializers.PrimaryKeyRelatedField(
        queryset=Plage.objects.all(),
        required=True
    )
    start_at = serializers.DateTimeField(required=True)
    end_at = serializers.DateTimeField(required=True)
    client_fname = serializers.CharField(required=True)
    client_lname = serializers.CharField(required=True)
    client_email = serializers.EmailField(required=True)
    client_phone = serializers.CharField(required=True)
    item = serializers.CharField(required=True)
    item_description = serializers.CharField(required=True)
    liability_accepted = serializers.BooleanField(required=True)

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