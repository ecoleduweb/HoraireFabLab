from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.services.slot_service import SlotService

service = SlotService()


@api_view(["POST"])
@permission_classes([])
def book_slot(request):
    try:
        slot = service.book_slot(request.data)
        return Response(slot, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)