from ingestion.models import Log
from detection.utils import *



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

