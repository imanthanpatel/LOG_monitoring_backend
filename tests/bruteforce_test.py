import requests
import time
import random
from datetime import datetime

URL = "http://127.0.0.1:8000/api/ingest/"

username = "admin"

# fake attacker IP (you can rotate this too)
ip_address = "192.168.1.100"

# brute force password list
passwords = [
    "123456",
    "password",
    "admin123",
    "test123",
    "qwerty",
    "letmein",
    "welcome",
    "admin@123",
    "pass123",
    "wrongpass"
]

print("🚨 Starting Brute Force Attack Simulation...\n")

for i, pwd in enumerate(passwords):

    payload = {
        # simulate Windows Event ID for failed login
        "event_id": 4625,

        # source system
        "source": "Windows Security",

        # type of log
        "log_type": "authentication_failed",

        # message similar to real logs
        "message": f"Failed login attempt for user '{username}' using password '{pwd}'",

        # keyword helps detection rules
        "keyword": "failed_login",

        # system where attempt happened
        "computer": "DESKTOP-ATTACKER",

        # user being attacked
        "username": username,

        # attacker IP
        "ip_address": ip_address,

        # simulate real timestamp
        "time_generated": datetime.utcnow().isoformat()
    }

    try:
        response = requests.post(URL, json=payload)

        print(f"[{i+1}] Attempt with password: {pwd}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}\n")

    except Exception as e:
        print(f"Error: {e}")

    # IMPORTANT: keep delay small to trigger brute-force window rule
    time.sleep(0.5)

print("✅ Brute force simulation completed.")