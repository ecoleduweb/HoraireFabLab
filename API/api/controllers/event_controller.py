from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.serializers.event_serializer import EventSerializer
from api.services.event_service import EventService
from api.models import Event

service = EventService()

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = Event(**serializer.validated_data)
        event = service.create_event(event)
        return Response(event, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_upcoming_events(request):
    try:
        events = service.get_upcoming_events()
        return Response(events, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
