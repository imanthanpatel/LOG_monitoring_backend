from ingestion.models import Log
from detection.utils import *
from detection.models import MitreTechnique

def resolve_mitre(mitre_code):
    obj = MitreTechnique.objects.filter(
        technique_id__iexact=mitre_code
    ).first()

    if not obj:
        obj = MitreTechnique.objects.filter(
            name__icontains=mitre_code
        ).first()

    return obj.technique_id if obj else None


# ==========================================
# RULE 8: Service Installation
# Event ID: 7045
# MITRE: T1543
# ==========================================

def service_installation():

    state = get_state("Service Installation")

    new_logs = Log.objects.filter(id__gt=state.last_processed_id)
    if not new_logs.exists():
        return

    for log in new_logs.filter(event_id=7045):
        create_alert(
            rule_name="Service Installation",
            severity="High",
            description=f"Service installed on {log.computer}",
            mitre=resolve_mitre("T1543")
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

    # ✅ FIX: safe MITRE resolution
    mitre_obj = resolve_mitre("T1053.005")

    for log in matched:
        create_alert(
            rule_name="Scheduled Task Created",
            severity="Medium",
            description=(
                f"Scheduled task created on {log.computer}. "
                f"User: {log.username or 'Unknown'}. "
                f"Details: {str(log.message)[:200]}"
            ),
            mitre=mitre_obj
        )

    advance_state(state, new_logs)

