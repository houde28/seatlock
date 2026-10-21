# Seatlock

Seatlock is a REST API for booking event seats, built to handle many users booking the same seat at the same moment without double-booking or server errors.

## Tech Stack
- Python, Django, Django REST Framework
- PostgreSQL (running in Docker Compose)
- Automated tests with DRF's APITestCase

## Features
- Browse events and seats (`GET /api/events/`, `GET /api/seats/`)
- Book a seat (`POST /api/bookings/`), login required
- Users can only see their own bookings
- Validation: a seat must belong to the event's venue
- Database-enforced rule: one booking per seat per event

## Running Locally
```bash
docker compose up -d
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Run the tests:
```bash
python manage.py test bookings
``` 

## Concurrency
When many users book the same seat at once, each request can pass the "is this seat free?" check before any of them saves. The database's unique constraint stops the double booking, but the rejected requests used to crash with server errors.

I wrote a script (`scripts/race_test.py`) that sends 20 simultaneous booking requests for the same seat, and added a temporary delay to force the race every time.

| | Result |
|---|---|
| Before fix | 1 × 201, 19 × 500 (server errors) |
| After fix | 1 × 201, 19 × 409 (clean conflict response) |

The fix: the save runs inside `transaction.atomic()`, and an `IntegrityError` from the database is caught and returned as a clear error instead of a crash.