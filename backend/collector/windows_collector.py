import win32evtlog
import requests
import time
import re
from datetime import datetime, timezone

# =========================
# CONFIG
# =========================

BACKEND_URL = "http://127.0.0.1:8000/api/ingest/"
POLL_INTERVAL = 5

LOG_TYPES = [
    "Security",
    "System",
    "Application",
    "Microsoft-Windows-PowerShell/Operational",
]

last_record = {log: 0 for log in LOG_TYPES}

# Events we actively watch and print debug for
WATCHED_EVENT_IDS = {
    4624,   # Successful logon
    4625,   # Failed logon
    4720,   # User account created
    4726,   # User account deleted
    4728,   # Member added to security group
    4104,   # PowerShell script block
    4688,   # New process created
    4698,   # Scheduled task created
}

# Noisy low-value events to skip entirely
IGNORED_EVENT_IDS = {
    5156,   # Firewall allowed connection
    5158,   # Firewall allowed bind
    4656,   # Object handle requested
    4658,   # Object handle closed
    4690,   # Object handle duplicated
    5447,   # WFP filter changed
}


# =========================
# EXTRACT USERNAME
# =========================

def extract_username(event_id, inserts):
    if not inserts:
        return None
    try:
        if event_id in [4624, 4625]:
            # Index 5 = TargetUserName
            return inserts[5] if len(inserts) > 5 else None

        elif event_id == 4688:
            # Index 1 = SubjectUserName
            return inserts[1] if len(inserts) > 1 else None

        elif event_id in [4720, 4726, 4728]:
            # Index 0 = TargetUserName
            return inserts[0] if len(inserts) > 0 else None

        elif event_id == 4104:
            # No direct username in PowerShell script block inserts
            return None

        elif event_id == 4698:
            # Index 1 = SubjectUserName for scheduled task
            return inserts[1] if len(inserts) > 1 else None

    except Exception:
        pass
    return None


# =========================
# PARSE EVENT
# =========================

def parse_event(event, log_type):
    event_id = event.EventID & 0xFFFF
    inserts = list(event.StringInserts or [])
    message = " ".join(str(x) for x in inserts)

    # Extract first IPv4 address found
    ip_address = None
    ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", message)
    if ips:
        ip_address = ips[0]

    username = extract_username(event_id, inserts)

    # Clean up system/machine accounts
    if username and (username.endswith("$") or username == "-" or username == "SYSTEM"):
        username = None

    return {
        "event_id": event_id,
        "source": event.SourceName,
        "computer": event.ComputerName,
        "username": username,
        "ip_address": ip_address,
        "message": message[:4000],
        "log_type": log_type,
        ""
        "time_generated": str(event.TimeGenerated),
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }


# =========================
# SEND LOG
# =========================

def send_log(data):
    try:
        r = requests.post(BACKEND_URL, json=data, timeout=5)
        if r.status_code in [200, 201]:
            print(
                f"[OK] EventID={data['event_id']} "
                f"User={data['username']} "
                f"Log={data['log_type']}"
            )
        else:
            print(f"[BACKEND ERROR] {r.status_code} {r.text}")
    except Exception as e:
        print(f"[CONNECTION ERROR] {e}")


# =========================
# READ LOGS
# =========================

def read_logs(log_name):
    global last_record

    try:
        handle = win32evtlog.OpenEventLog(None, log_name)
    except Exception as e:
        print(f"[OPEN ERROR] {log_name}: {e}")
        return

    flags = (
        win32evtlog.EVENTLOG_BACKWARDS_READ |
        win32evtlog.EVENTLOG_SEQUENTIAL_READ
    )

    new_events = []

    try:
        while True:
            batch = win32evtlog.ReadEventLog(handle, flags, 0)
            if not batch:
                break

            reached_old = False
            for event in batch:
                record_id = event.RecordNumber
                if record_id <= last_record[log_name]:
                    reached_old = True
                    break
                new_events.append(event)

            if reached_old:
                break

    except Exception as e:
        print(f"[READ ERROR] {log_name}: {e}")
    finally:
        win32evtlog.CloseEventLog(handle)

    if not new_events:
        return

    # Process oldest first (list is newest-first due to BACKWARDS_READ)
    for event in reversed(new_events):
        record_id = event.RecordNumber
        if record_id > last_record[log_name]:
            last_record[log_name] = record_id

        eid = event.EventID & 0xFFFF

        # Skip noisy events
        if eid in IGNORED_EVENT_IDS:
            continue

        # Print debug for watched events
        if eid in WATCHED_EVENT_IDS:
            print("\n" + "=" * 60)
            print(f"[ALERT] EventID={eid} | Log={log_name}")
            print(f"        Source  : {event.SourceName}")
            print(f"        Computer: {event.ComputerName}")
            print(f"        Time    : {event.TimeGenerated}")

            LABELS = {
                4624: "Successful Logon",
                4625: "Failed Logon",
                4720: "User Account Created",
                4726: "User Account Deleted",
                4728: "Member Added to Group",
                4104: "PowerShell Script Block",
                4688: "New Process Created",
                4698: "Scheduled Task Created",
            }
            print(f"        Type    : {LABELS.get(eid, 'Unknown')}")

            if event.StringInserts:
                print("        Inserts :")
                for i, item in enumerate(event.StringInserts):
                    print(f"          [{i}] {item}")
            else:
                print("        No StringInserts")
            print("=" * 60)

        log_data = parse_event(event, log_name)
        send_log(log_data)


# =========================
# INITIALIZE OFFSETS
# =========================

def initialize_offsets():
    print("[*] Initializing log offsets (skipping historical events)...")
    for log_name in LOG_TYPES:
        try:
            handle = win32evtlog.OpenEventLog(None, log_name)
            flags = (
                win32evtlog.EVENTLOG_BACKWARDS_READ |
                win32evtlog.EVENTLOG_SEQUENTIAL_READ
            )
            batch = win32evtlog.ReadEventLog(handle, flags, 0)
            if batch:
                last_record[log_name] = batch[0].RecordNumber
                print(f"    {log_name}: starting at record {last_record[log_name]}")
            else:
                print(f"    {log_name}: empty log")
            win32evtlog.CloseEventLog(handle)
        except Exception as e:
            print(f"    [SKIP] {log_name}: {e}")


# =========================
# MAIN LOOP
# =========================

def start_collector():
    print("\n Windows Event Collector Started")
    print("=" * 60)
    print("Monitoring logs:")
    for log in LOG_TYPES:
        print(f"  - {log}")
    print("=" * 60)

    print("\nWatching for EventIDs:")
    for eid in sorted(WATCHED_EVENT_IDS):
        print(f"  - {eid}")
    print("=" * 60)

    initialize_offsets()
    print("\n[*] Now watching for new events...\n")

    while True:
        try:
            for log in LOG_TYPES:
                read_logs(log)
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\n[*] Collector stopped by user.")
            break
        except Exception as e:
            print(f"[COLLECTOR CRASH] {e}")
            time.sleep(5)


# =========================
# START
# =========================

if __name__ == "__main__":
    start_collector()