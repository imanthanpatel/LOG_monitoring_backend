from ingestion.models import Log
from detection.utils import *




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