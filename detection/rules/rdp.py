from ingestion.models import Log
from detection.utils import (
    create_alert,
    get_state,
    advance_state,
    get_severity,
    extract_ip,
)




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
