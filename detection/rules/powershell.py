from ingestion.models import Log
from detection.utils import *
from detection.models import MitreTechnique


# ==========================================
# RULE 3: PowerShell Execution
# ==========================================

def powershell_execution():

    state = get_state("PowerShell Execution")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    matched = new_logs.filter(event_id=4104)

    # FIX: safe MITRE resolution
    mitre_obj = MitreTechnique.objects.filter(
        technique_id__iexact="T1059.001"
    ).first()

    if not mitre_obj:
        mitre_obj = MitreTechnique.objects.filter(
            name__icontains="powershell"
        ).first()

    for log in matched:
        create_alert(
            rule_name="PowerShell Execution",
            severity="High",
            description=(
                f"PowerShell script block executed on {log.computer}. "
                f"Preview: {str(log.message)[:200]}"
            ),
            mitre=mitre_obj.technique_id if mitre_obj else None
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 4: Suspicious PowerShell Keywords
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

    # FIX: safe MITRE resolution
    mitre_obj = MitreTechnique.objects.filter(
        technique_id__iexact="T1059.001"
    ).first()

    if not mitre_obj:
        mitre_obj = MitreTechnique.objects.filter(
            name__icontains="powershell"
        ).first()

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
                mitre=mitre_obj.technique_id if mitre_obj else None
            )

    advance_state(state, new_logs)