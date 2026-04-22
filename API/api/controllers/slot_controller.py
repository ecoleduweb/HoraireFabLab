from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.models import Slot
from api.serializers.slot_serializer import SlotSerializer
from api.services.slot_service import SlotService

@api_view(["POST"])
#Permet d'accéder à la route sans être authentifié car réserver un rendez-vous ne nécessite pas de 
@permission_classes([])
def book_slot(request):
    try:
        serializer = SlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        slot = Slot(
            plage=validated["plage"],
            start_at=validated["start_at"],
            end_at=validated["end_at"],
            client_fname=validated.get("client_fname"),
            client_lname=validated.get("client_lname"),
            client_email=validated.get("client_email"),
            client_phone=validated.get("client_phone"),
            item=validated.get("item"),
            item_description=validated.get("item_description"),
            liability_accepted=validated.get("liability_accepted", False),
        )
        service = SlotService()
        slot = service.book_slot(slot)
        return Response(slot, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)