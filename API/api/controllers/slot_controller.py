from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse

from api.models import Slot
from api.serializers.slot_serializer import SlotSerializer
from api.serializers.available_slot_serializer import AvailableSlotSerializer
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

@api_view(["GET"])
@permission_classes([])
def get_available_slots(request, event_id):
    service = SlotService()
    slots = service.get_available_slots(event_id)
    serializer = AvailableSlotSerializer(slots, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
        
    