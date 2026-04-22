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
        slot = Slot(**serializer.validated_data)
        service = SlotService()
        slot = service.book_slot(slot)
        return Response(slot, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)