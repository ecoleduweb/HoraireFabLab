from rest_framework import serializers
from api.models import Slot, Plage
import nh3


def sanitize(value: str) -> str:
    return nh3.clean(value, tags=set())


class SlotSerializer(serializers.ModelSerializer):
    plage = serializers.PrimaryKeyRelatedField(
        queryset=Plage.objects.all(),
        required=True
    )

    #mapping pour que les données avec les champs en camelCase de la requête marchent avec le snake_case interne de l'API
    # startAt = serializers.DateTimeField(source="start_at", required=True)
    # endAt = serializers.DateTimeField(source="end_at", required=True)

    # clientFname = serializers.CharField(source="client_fname", required=True)
    # clientLname = serializers.CharField(source="client_lname", required=True)
    # clientEmail = serializers.EmailField(source="client_email", required=True)
    # clientPhone = serializers.CharField(source="client_phone", required=True)

    # item = serializers.CharField(required=True)
    # itemDescription = serializers.CharField(source="item_description", required=True)

    # liabilityAccepted = serializers.BooleanField(source="liability_accepted", required=True)

    # isCanceled = serializers.BooleanField(source="is_canceled", read_only=True)
    # createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    # updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Slot
        fields = [
            "id",
            "plage",
            "startAt",
            "endAt",
            "clientFname",
            "clientLname",
            "clientEmail",
            "clientPhone",
            "item",
            "itemDescription",
            "liabilityAccepted",
            "isCanceled",
            "updatedAt",
            "createdAt",
        ]
        read_only_fields = ["id", "createdAt", "updatedAt", "isCanceled"]

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