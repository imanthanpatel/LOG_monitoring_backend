from ingestion.models import Log
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from detection.utils import *

from detection.config import (
    BRUTEFORCE_THRESHOLD,
    BRUTEFORCE_WINDOW_MINUTES,
)

from detection.models import MitreTechnique

RULE_INFO = {
    "name": "Brute Force Detection",
    "severity": "High",
    "mitre": "T1110",
    "description": "Multiple failed login attempts"
}


# ==========================================
# RULE 1: Brute Force Detection
# Event ID: 4625
# MITRE: T1110
# FIX: Was alerting on >5 but window was
# all-time, not time-based. Now uses
# a 5-minute sliding window.
# ==========================================

def detect_bruteforce():

    state = get_state("Brute Force Detection")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    # Count failed logins in last 5 minutes
    window = timezone.now() - timedelta(
        minutes=BRUTEFORCE_WINDOW_MINUTES
    )

    failed = Log.objects.filter(
        event_id=4625,
        time_generated__gte=window
    )

    count = failed.count()

    if count >= BRUTEFORCE_THRESHOLD:
        # Group by username to show who is being targeted
        usernames = list(
            failed.exclude(username=None)
            .values_list("username", flat=True)
            .distinct()
        )

        ips = list(set(
            filter(
                    None,
                    [extract_ip(log) for log in failed]
    )
))

        desc = (
            f"{count} failed logins in 5 minutes. "
            f"Targets: {', '.join(usernames) if usernames else 'Unknown'}. "
            f"Source IPs: {', '.join(ips) if ips else 'Unknown'}."
        )

        mitre = MitreTechnique.objects.get(
                technique_id="T1110"
)

        create_alert(
            rule_name=RULE_INFO["name"],
            severity=get_severity(count),
            description=desc,
            mitre=mitre
        )

    advance_state(state, new_logs)


# ==========================================
# RULE 2: Brute Force then Success
# Event IDs: 4625 followed by 4624
# MITRE: T1110.001
# NEW: Detects successful login after
# multiple failures — likely compromise.
# ==========================================

def detect_bruteforce_success():

    state = get_state("Brute Force Success")

    new_logs = Log.objects.filter(
        id__gt=state.last_processed_id
    )

    if not new_logs.exists():
        return

    window = timezone.now() - timedelta(minutes=10)

    # Find usernames that had 3+ failures
    failed = Log.objects.filter(
        event_id=4625,
        time_generated__gte=window
    ).exclude(username=None)

    
    risky_users = (
        failed.values("username")
        .annotate(fail_count=Count("id"))
        .filter(fail_count__gte=3)
        .values_list("username", flat=True)
    )

    if not risky_users:
        advance_state(state, new_logs)
        return

    # Check if any of those users then succeeded
    success = Log.objects.filter(
        event_id=4624,
         time_generated__gte=window,
        username__in=risky_users
    )

    if success.exists():
        for s in success:
            create_alert(
                rule_name="Brute Force Success",
                severity="Critical",
                description=(
                    f"User '{s.username}' logged in successfully "
                    f"after multiple failed attempts. "
                    f"Possible account compromise. IP: {s.ip_address}"
                ),
                mitre="T1110.001"
            )

    advance_state(state, new_logs)
