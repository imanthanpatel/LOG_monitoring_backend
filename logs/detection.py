from .models import (
    Log,
    Alert,
    Incident,
    DetectionState
)
from django.utils import timezone
from datetime import timedelta

import re
from django.db.models import Count

def extract_ip(log):
    if log.ip_address:
        return log.ip_address

    msg = log.message or ""

    match = re.search(
        r'([0-9a-fA-F:\.]+)\s+\d+\s*$',
        msg
    )

    if match:
        ip = match.group(1)

        if ip == "::1":
            return "127.0.0.1"

        return ip

    return None

# ==========================================
# Alert + Incident Creator
# ==========================================

def create_alert(rule_name, severity, description, mitre=None, log=None):

    # Prevent duplicate alerts for the same rule
    duplicate_window = timezone.now() - timedelta(minutes=5)

    existing = Alert.objects.filter(
        rule_name=rule_name,
        description=description,
        timestamp__gte=duplicate_window
    ).first()

    if existing:
        return existing

    alert = Alert.objects.create(
        rule_name=rule_name,
        severity=severity,
        description=description,
        mitre_technique=mitre,
    )

    Incident.objects.create(
        alert=alert,
        status="Open"
    )

    return alert

# ==========================================
# Detection State
# ==========================================

def get_state(rule_name):

    state, _ = DetectionState.objects.get_or_create(
        rule_name=rule_name,
        defaults={"last_processed_id": 0}
    )

    return state


def advance_state(state, new_logs):
    latest = new_logs.order_by("-id").first()
    if latest:
        state.last_processed_id = latest.id
        state.save()


# ==========================================
# Dynamic Severity
# ==========================================

def get_severity(count):
    if count > 20:
        return "Critical"
    if count > 10:
        return "High"
    if count > 5:
        return "Medium"
    return "Low"


# ==========================================
# RULE 1: Brute Force Detection
# Event ID: 4625
# MITRE: T1110
# FIX: Was alerting on >5 but window was
# all-time, not time-based. Now uses
# a 5-minute sliding window.
# ==========================================

def detect_bruteforce():

    state = get_state("Brute Force Detection")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    # Count failed logins in last 5 minutes
    window = timezone.now() - timedelta(minutes=5)

    failed = Log.objects.filter(
        event_id=4625,
        time_generated__gte=window
    )

    count = failed.count()

    if count >= 5:
        # Group by username to show who is being targeted
        usernames = list(
            failed.exclude(username=None)
            .values_list("username", flat=True)
            .distinct()
        )

        ips = list(set(
            filter(
                    None,
                    [extract_ip(log) for log in failed]
    )
))

        desc = (
            f"{count} failed logins in 5 minutes. "
            f"Targets: {', '.join(usernames) if usernames else 'Unknown'}. "
            f"Source IPs: {', '.join(ips) if ips else 'Unknown'}."
        )

        create_alert(
            rule_name="Brute Force Detection",
            severity=get_severity(count),
            description=desc,
            mitre="T1110"
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 2: Brute Force then Success
# Event IDs: 4625 followed by 4624
# MITRE: T1110.001
# NEW: Detects successful login after
# multiple failures — likely compromise.
# ==========================================

def detect_bruteforce_success():

    state = get_state("Brute Force Success")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    window = timezone.now() - timedelta(minutes=10)

    # Find usernames that had 3+ failures
    failed = Log.objects.filter(
        event_id=4625,
        time_generated__gte=window
    ).exclude(username=None)

    
    risky_users = (
        failed.values("username")
        .annotate(fail_count=Count("id"))
        .filter(fail_count__gte=3)
        .values_list("username", flat=True)
    )

    if not risky_users:
        advance_state(state, new_logs)
        return

    # Check if any of those users then succeeded
    success = Log.objects.filter(
        event_id=4624,
         time_generated__gte=window,
        username__in=risky_users
    )

    if success.exists():
        for s in success:
            create_alert(
                rule_name="Brute Force Success",
                severity="Critical",
                description=(
                    f"User '{s.username}' logged in successfully "
                    f"after multiple failed attempts. "
                    f"Possible account compromise. IP: {s.ip_address}"
                ),
                mitre="T1110.001"
            )

    advance_state(state, new_logs)


# ==========================================
# RULE 3: PowerShell Execution
# Event ID: 4104
# MITRE: T1059.001
# ==========================================

def powershell_execution():

    state = get_state("PowerShell Execution")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    matched = new_logs.filter(event_id=4104)

    for log in matched:
        create_alert(
            rule_name="PowerShell Execution",
            severity="High",
            description=(
                f"PowerShell script block executed on {log.computer}. "
                f"Preview: {str(log.message)[:200]}"
            ),
            mitre="T1059.001"
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 4: Suspicious PowerShell Keywords
# Event ID: 4104
# MITRE: T1059.001
# NEW: Flags encoded commands, downloads,
# credential dumping patterns.
# ==========================================

SUSPICIOUS_PS_KEYWORDS = [
    "invoke-expression",
    "iex(",
    "downloadstring",
    "webclient",
    "encodedcommand",
    "-enc ",
    "mimikatz",
    "invoke-mimikatz",
    "sekurlsa",
    "net user",
    "net localgroup",
    "bypass",
    "hidden",
    "frombase64string",
]

def suspicious_powershell():

    state = get_state("Suspicious PowerShell")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    matched = new_logs.filter(event_id=4104)

    for log in matched:
        msg = (log.message or "").lower()
        hits = [kw for kw in SUSPICIOUS_PS_KEYWORDS if kw in msg]

        if hits:
            create_alert(
                rule_name="Suspicious PowerShell",
                severity="Critical",
                description=(
                    f"Suspicious PowerShell detected on {log.computer}. "
                    f"Keywords matched: {', '.join(hits)}. "
                    f"Preview: {str(log.message)[:300]}"
                ),
                mitre="T1059.001"
            )

    advance_state(state, new_logs)


# ==========================================
# RULE 5: New User Creation
# Event ID: 4720
# MITRE: T1136
# ==========================================

def new_user_creation():

    state = get_state("New User Creation")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    matched = new_logs.filter(event_id=4720)

    for log in matched:
        create_alert(
            rule_name="New User Creation",
            severity="Medium",
            description=(
                f"New user account created on {log.computer}. "
                f"Username: {log.username or 'Unknown'}"
            ),
            mitre="T1136"
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 6: User Account Deleted
# Event ID: 4726
# MITRE: T1531
# ==========================================

def deleting_user():

    state = get_state("User Deleted")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    matched = new_logs.filter(event_id=4726)

    for log in matched:
        create_alert(
            rule_name="User Deleted",
            severity="High",
            description=(
                f"User account deleted on {log.computer}. "
                f"Username: {log.username or 'Unknown'}"
            ),
            mitre="T1531"
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 7: RDP / Successful Logon
# Event ID: 4624
# MITRE: T1021.001
# FIX: Only alert on Logon Type 10 (RDP)
# not every single login
# ==========================================

def rdp_login():

    state = get_state("RDP Login")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    # Logon Type 10 = RemoteInteractive (RDP)
    # Message contains "10" as logon type in inserts
    matched = new_logs.filter(
        event_id=4624,
        message__contains="10"
    )

    for log in matched:
        create_alert(
            rule_name="RDP Login",
            severity="Medium",
            description=(
                f"RDP login detected on {log.computer}. "
                f"User: {log.username or 'Unknown'}. "
                f"Source IP: {log.ip_address or 'Unknown'}"
            ),
            mitre="T1021.001"
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 8: Service Installation
# Event ID: 7045
# MITRE: T1543
# ==========================================

def service_installation():

    state = get_state("Service Installation")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    matched = new_logs.filter(event_id=7045)

    for log in matched:
        create_alert(
            rule_name="Service Installation",
            severity="High",
            description=(
                f"New Windows service installed on {log.computer}. "
                f"Details: {str(log.message)[:200]}"
            ),
            mitre="T1543"
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 9: Scheduled Task Created
# Event ID: 4698
# MITRE: T1053.005
# NEW
# ==========================================

def scheduled_task_created():

    state = get_state("Scheduled Task Created")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    matched = new_logs.filter(event_id=4698)

    for log in matched:
        create_alert(
            rule_name="Scheduled Task Created",
            severity="Medium",
            description=(
                f"Scheduled task created on {log.computer}. "
                f"User: {log.username or 'Unknown'}. "
                f"Details: {str(log.message)[:200]}"
            ),
            mitre="T1053.005"
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 10: Suspicious Process Creation
# Event ID: 4688
# MITRE: T1059
# NEW: Flags high-risk process names
# ==========================================

SUSPICIOUS_PROCESSES = [
    "mimikatz.exe",
    "procdump.exe",
    "wce.exe",
    "fgdump.exe",
    "pwdump.exe",
    "nc.exe",
    "ncat.exe",
    "psexec.exe",
    "psexesvc.exe",
    "wmic.exe",
    "mshta.exe",
    "regsvr32.exe",
    "rundll32.exe",
    "certutil.exe",
    "bitsadmin.exe",
]

def suspicious_process():

    state = get_state("Suspicious Process")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    matched = new_logs.filter(event_id=4688)

    for log in matched:
        msg = (log.message or "").lower()
        hits = [p for p in SUSPICIOUS_PROCESSES if p in msg]

        if hits:
            create_alert(
                rule_name="Suspicious Process",
                severity="Critical",
                description=(
                    f"Suspicious process detected on {log.computer}. "
                    f"Process: {', '.join(hits)}. "
                    f"User: {log.username or 'Unknown'}"
                ),
                mitre="T1059"
            )

    advance_state(state, new_logs)


# ==========================================
# RULE 11: Off-Hours Login
# Event ID: 4624
# MITRE: T1078
# NEW: Login outside 8am-8pm
# ==========================================

def off_hours_login():

    state = get_state("Off Hours Login")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    matched = new_logs.filter(event_id=4624)

    for log in matched:

        if not log.time_generated:
            continue

        hour = log.time_generated.hour

        if hour >= 22 or hour < 6:

            create_alert(
                rule_name="Off Hours Login",
                severity="Medium",
                description=(
                    f"Login detected outside business hours on {log.computer}. "
                    f"User: {log.username or 'Unknown'}. "
                    f"Time (UTC): {log.time_generated}. "
                    f"IP: {log.ip_address or 'Unknown'}"
                ),
                mitre="T1078"
            )

    advance_state(state, new_logs)


# ==========================================
# RUN ALL RULES
# Call this from your task scheduler
# or management command
# ==========================================

def run_all_rules():
    detect_bruteforce()
    detect_bruteforce_success()
    powershell_execution()
    suspicious_powershell()
    new_user_creation()
    deleting_user()
    rdp_login()
    service_installation()
    scheduled_task_created()
    suspicious_process()
    off_hours_login()