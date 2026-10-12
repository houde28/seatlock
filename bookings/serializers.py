from .models import Booking
from rest_framework import serializers

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'event', 'seat', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, attrs):
        if attrs["seat"].venue != attrs["event"].venue:
            raise serializers.ValidationError("Seat does not belong to this event.")

        return attrs
