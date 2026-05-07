from api.models import Event
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.services.event_service import EventService
from api.serializers.event_serializer import EventSerializer
import logging


service = EventService()
logger = logging.getLogger(__name__)

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
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        logger.exception("Erreur inattendue dans get_events")
        return Response({"detail": "Erreur interne du serveur."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_upcoming_events(request):
    try:
        events = service.get_upcoming_events()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception :
        return Response("Erreur lors de la récupération des événements à venir", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_event_by_id(request, event_id):
    try:
        event = service.get_event_by_id(event_id)
        if event is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        logger.exception("Erreur inattendue dans get_event_by_id")
        return Response({"detail": "Erreur interne du serveur."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
