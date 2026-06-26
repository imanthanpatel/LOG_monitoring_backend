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
# RULE 5: New User Creation
# Event ID: 4720
# MITRE: T1136
# ==========================================

def new_user_creation():

    state = get_state("New User Creation")

    new_logs = Log.objects.filter(id__gt=state.last_processed_id)
    if not new_logs.exists():
        return

    for log in new_logs.filter(event_id=4720):
        create_alert(
            rule_name="New User Creation",
            severity="Medium",
            description=f"User created: {log.username}",
            mitre=resolve_mitre("T1136")
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 6: User Account Deleted
# Event ID: 4726
# MITRE: T1531
# ==========================================

def deleting_user():

    state = get_state("User Deleted")

    new_logs = Log.objects.filter(id__gt=state.last_processed_id)
    if not new_logs.exists():
        return

    for log in new_logs.filter(event_id=4726):
        create_alert(
            rule_name="User Deleted",
            severity="High",
            description=f"User deleted: {log.username}",
            mitre=resolve_mitre("T1531")
        )

    advance_state(state, new_logs)
