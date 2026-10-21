from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

import threading
from django.db import connection
from django.test import TransactionTestCase
from events.models import Venue, Event, Seat
from .models import Booking

class BookingTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username  ='usera', password = 'pass12345')
        self.venueA = Venue.objects.create(name = "test_venue1", address = "123 street")
        self.venueB = Venue.objects.create(name = "test_venue2", address = "456 street")

        self.eventA = Event.objects.create(name = "test_event1", start_time = "2026-11-01T19:00:00Z", venue=self.venueA)

        self.seatAtA = Seat.objects.create(venue = self.venueA, section = "A", row = "1", seat_number = "1")
        self.seatAtB = Seat.objects.create(venue = self.venueB, section = "B", row = "1", seat_number = "1")

        self.url = "/api/bookings/"
        self.client.force_authenticate(user=self.user)

    def test_unauthenticated_returns_401_or_403(self):
        self.client.force_authenticate(user=None)
        data = {"event": self.eventA.id, "seat": self.seatAtA.id}
        response = self.client.post(self.url, data, format="json")
        self.assertIn(response.status_code, [401,403])
    
    def test_valid_booking_returns_201(self):
        data = {"event": self.eventA.id, "seat": self.seatAtA.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wrong_venue_returns_400(self):
        data = {"event": self.eventA.id, "seat": self.seatAtB.id}
        response = self.client.post(self.url, data, format = "json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_booking_returns_409(self):
        data = {"event": self.eventA.id, "seat": self.seatAtA.id}
        first = self.client.post(self.url, data, format="json")
        second = self.client.post(self.url, data, format="json")
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_409_CONFLICT)
    
class ConcurrentBookingTest(TransactionTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='usera', password='pass12345')
        self.venueA = Venue.objects.create(name="test_venue1", address="123 street")
        self.eventA = Event.objects.create(name="test_event1", start_time="2026-11-01T19:00:00Z", venue=self.venueA)
        self.seatAtA = Seat.objects.create(venue=self.venueA, section="A", row="1", seat_number="1")
        self.url = "/api/bookings/"

    def test_only_one_concurrent_booking_succeeds(self):
        n = 10
        barrier = threading.Barrier(n)
        results = []
        results_lock = threading.Lock()

        def attempt():
            client = APIClient()
            client.force_authenticate(user=self.user)
            barrier.wait(timeout=10)
            response = client.post(
                self.url,
                {"event": self.eventA.id, "seat": self.seatAtA.id},
                format="json",
            )
            with results_lock:
                results.append(response.status_code)
            connection.close()

        threads = [threading.Thread(target=attempt) for _ in range(n)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(results.count(201), 1)
        self.assertEqual(results.count(409), n-1)
        self.assertEqual(Booking.objects.count(), 1)