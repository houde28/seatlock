from rest_framework import viewsets
from .models import Event, Seat
from .serializers import EventSerializer, SeatSerializer

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows events to be viewed.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer

class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows seats to be viewed.
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer



