from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from django.db import IntegrityError, transaction
from rest_framework.exceptions import APIException

class SeatAlreadyBooked(APIException):
    status_code = 409
    default_detail = "This seat is already booked for this event."
    default_code = "seat_already_booked"

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save(user=self.request.user)
        except IntegrityError:
            raise SeatAlreadyBooked()
