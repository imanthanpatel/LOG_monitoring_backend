from ingestion.models import Log
from detection.utils import *


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