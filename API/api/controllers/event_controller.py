from api.models import Event
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.services.event_service import EventService
from api.serializers.event_serializer import EventSerializer


service = EventService()

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_event(request, event_id):
    try:
        if not service.get_event_by_id(event_id):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = Event(**serializer.validated_data)
        event.id = event_id
        result = service.update_event(event)
        return Response(result, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


   

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

def get_events(request):
    try:
        events = service.get_all_events()
        return Response(events, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def get_upcoming_events(request):
    try:
        events = service.get_upcoming_events()
        return Response(events, status=status.HTTP_200_OK)
    except Exception :
        return Response("Erreur lors de la récupération des événements à venir", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
