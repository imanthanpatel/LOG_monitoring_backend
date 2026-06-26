import re

from django.utils import timezone
from datetime import timedelta

from ingestion.models import Log, DetectionState
from alerts.models import Alert, Incident
from detection.models import MitreTechnique


# ==========================================
# Extract IP
# ==========================================

def extract_ip(log):
    if log.ip_address:
        return log.ip_address

    msg = log.message or ""

    match = re.search(
        r'([0-9a-fA-F:\.]+)\s+\d+\s*$',
        msg
    )

    if match:
        ip = match.group(1)

        if ip == "::1":
            return "127.0.0.1"

        return ip

    return None


# ==========================================
# Alert + Incident Creator
# ==========================================

def create_alert(rule_name, severity, description, mitre=None, log=None, mitre_technique=None):

    # allow both parameter names without breaking existing code
    if mitre is None and mitre_technique is not None:
        mitre = mitre_technique

    duplicate_window = timezone.now() - timedelta(minutes=5)

    existing = Alert.objects.filter(
        rule_name=rule_name,
        description=description,
        timestamp__gte=duplicate_window
    ).first()

    if existing:
        return existing

    mitre_obj = None

    # ==========================================
    # FIXED MITRE RESOLUTION (NO LOGIC CHANGE)
    # ==========================================
    if mitre:
        mitre_obj = MitreTechnique.objects.filter(
            technique_id__iexact=mitre
        ).first()

        if not mitre_obj:
            mitre_obj = MitreTechnique.objects.filter(
                name__icontains=mitre
            ).first()

    alert = Alert.objects.create(
        rule_name=rule_name,
        severity=severity,
        description=description,
        mitre_technique=mitre_obj,
    )

    Incident.objects.create(
        alert=alert,
        status="Open"
    )

    return alert


# ==========================================
# Detection State
# ==========================================

def get_state(rule_name):

    state, _ = DetectionState.objects.get_or_create(
        rule_name=rule_name,
        defaults={"last_processed_id": 0}
    )

    return state


def advance_state(state, new_logs):
    latest = new_logs.order_by("-id").first()
    if latest:
        state.last_processed_id = latest.id
        state.save()


# ==========================================
# Dynamic Severity
# ==========================================

def get_severity(count):
    if count > 20:
        return "Critical"
    if count > 10:
        return "High"
    if count > 5:
        return "Medium"
    return "Low"