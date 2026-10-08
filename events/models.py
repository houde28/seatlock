from django.db import models

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=75)

    def __str__(self):
        return f"{self.name} at ({self.address})"

class Event(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} at {self.venue.name}, starting at {self.start_time}"

class Seat(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    section = models.CharField(max_length=4)
    row = models.IntegerField()
    seat_number = models.IntegerField()

    def __str__(self):
        return f"{self.venue.name}, Section {self.section}, Row {self.row}, Seat {self.seat_number}"
 
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["venue", "section", "row", "seat_number"],
                name = "unique_seat_per_venue",
            )
        ]
