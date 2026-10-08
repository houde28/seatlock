from django.db import models
from django.conf import settings

class Booking(models.Model):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    seat = models.ForeignKey("events.Seat", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields = ['event', 'seat', 'user', 'created_at'],
            name = 'unique_seat_per_event',
            )
        ]