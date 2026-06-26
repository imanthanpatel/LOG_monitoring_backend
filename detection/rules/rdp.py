from ingestion.models import Log
from detection.utils import (
    create_alert,
    get_state,
    advance_state,
    get_severity,
    extract_ip,
)

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
# RULE 7: RDP / Successful Logon
# Event ID: 4624
# MITRE: T1021.001
# FIX: Only alert on Logon Type 10 (RDP)
# not every single login
# ==========================================

def rdp_login():

    state = get_state("RDP Login")

    new_logs = Log.objects.filter(id__gt=state.last_processed_id)
    if not new_logs.exists():
        return

    for log in new_logs.filter(event_id=4624, message__contains="10"):
        create_alert(
            rule_name="RDP Login",
            severity="Medium",
            description=f"RDP login: {log.username}",
            mitre=resolve_mitre("T1021.001")
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

    new_logs = Log.objects.filter(id__gt=state.last_processed_id)
    if not new_logs.exists():
        return

    for log in new_logs.filter(event_id=4624):

        if log.time_generated:
            hour = log.time_generated.hour

            if hour >= 22 or hour < 6:
                create_alert(
                    rule_name="Off Hours Login",
                    severity="Medium",
                    description=f"Off-hours login by {log.username}",
                    mitre=resolve_mitre("T1078")
                )

    advance_state(state, new_logs)
