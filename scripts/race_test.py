import threading
from collections import Counter
import requests

URL = "http://127.0.0.1:8000/api/bookings/"
AUTH = ("ex_username", "ex_password")
DATA = {"event": 1, "seat": 1}

results = []

def book():
    r = requests.post(URL, json = DATA, auth = AUTH)
    results.append(r.status_code)

threads = [threading.Thread(target = book) for _ in range(20)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(Counter(results))