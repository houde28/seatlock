from django.contrib import admin
from .models import Venue, Event, Seat

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'venue')
    search_fields = ('name', 'start_time', 'venue')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('venue', 'section', 'row', 'seat_number')
    search_fields = ('venue', 'section', 'row', 'seat_number')
