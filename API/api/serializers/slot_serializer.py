from rest_framework import serializers
from api.models import Slot, Plage
from api.utils.sanitize import sanitize


class SlotSerializer(serializers.ModelSerializer):
    plage = serializers.PrimaryKeyRelatedField(
        queryset=Plage.objects.all(),
        required=True
    )

    #mapping pour que les données avec les champs en camelCase de la requête marchent avec le snake_case interne de l'API
    start_at = serializers.DateTimeField(required=True)
    end_at = serializers.DateTimeField(required=True)

    client_fname = serializers.CharField(required=True)
    client_lname = serializers.CharField(required=True)
    client_email = serializers.EmailField(required=True)
    client_phone = serializers.CharField(required=True)

    item = serializers.CharField(required=True)
    item_description = serializers.CharField(required=True)

    liability_accepted = serializers.BooleanField(required=True)

    is_canceled = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Slot
        fields = [
            "id",
            "plage",
            "start_at",
            "end_at",
            "client_fname",
            "client_lname",
            "client_email",
            "client_phone",
            "item",
            "item_description",
            "liability_accepted",
            "is_canceled",
            "updated_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_canceled"]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        text_fields = [
            'client_fname',
            'client_lname',
            'client_email',
            'client_phone',
            'item',
            'item_description'
        ]

        for field in text_fields:
            if field in ret and isinstance(ret[field], str):
                ret[field] = sanitize(ret[field])

        return ret