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