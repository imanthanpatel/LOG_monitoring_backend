from ingestion.models import Log
from detection.utils import *



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