import requests
import time
from datetime import datetime

URL = "http://127.0.0.1:8000/api/ingest/"

def send(data):
    requests.post(URL, json=data)


# ==========================================
# 1. BRUTE FORCE
# ==========================================

for i in range(10):
    send({
        "event_id": 4625,
        "username": "admin",
        "ip_address": "192.168.1.100",
        "message": "failed login"
    })
    time.sleep(0.3)


# ==========================================
# 2. SUCCESS LOGIN
# ==========================================

send({
    "event_id": 4624,
    "username": "admin",
    "ip_address": "192.168.1.100",
    "message": "successful login"
})


# ==========================================
# 3. POWERSHELL ATTACK
# ==========================================

send({
    "event_id": 4104,
    "computer": "PC-1",
    "message": "IEX(New-Object Net.WebClient)"
})


# ==========================================
# 4. SUSPICIOUS PROCESS
# ==========================================

send({
    "event_id": 4688,
    "computer": "PC-1",
    "message": "rundll32.exe malicious"
})


# ==========================================
# 5. USER CREATION
# ==========================================

send({
    "event_id": 4720,
    "username": "hacker"
})


# ==========================================
# 6. USER DELETE
# ==========================================

send({
    "event_id": 4726,
    "username": "admin"
})


# ==========================================
# 7. RDP LOGIN
# ==========================================

send({
    "event_id": 4624,
    "username": "admin",
    "message": "Logon Type 10"
})


# ==========================================
# 8. OFF HOURS LOGIN
# ==========================================

send({
    "event_id": 4624,
    "username": "admin",
    "time_generated": "2026-06-26T02:30:00Z"
})


print("✅ SIEM attack simulation completed")