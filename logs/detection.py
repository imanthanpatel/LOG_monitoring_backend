from .models import Log, Alert, DetectionState


def get_state(rule_name):
    state, _ = DetectionState.objects.get_or_create(
        rule_name=rule_name,
        defaults={"last_processed_id": 0}
    )
    return state


def get_severity(count):

    if count > 20:
        return "Critical"

    if count > 10:
        return "High"

    if count > 5:
        return "Medium"

    return "Low"


def detect_bruteforce():

    state = get_state("Brute Force")

    failed_logs = Log.objects.filter(
        event_id=4625,
        id__gt=state.last_processed_id
    )

    count = failed_logs.count()

    if count > 5:

        severity = get_severity(count)

        Alert.objects.get_or_create(
        rule_name="Brute Force",
        description=f"{count} failed logins detected",
        defaults={
            "severity": severity
            }
)

    latest = failed_logs.order_by("-id").first()

    if latest:
        state.last_processed_id = latest.id
        state.save()


def powershell_execution():

    state = get_state("PowerShell Execution")

    logs = Log.objects.filter(
        source__iexact="powershell.exe",
        id__gt=state.last_processed_id
    )

    if logs.exists():

       Alert.objects.get_or_create(
        rule_name="PowerShell Execution",
        description="PowerShell execution detected",
        defaults={"severity": "High"}
)

    latest = Log.objects.order_by("-id").first()

    if latest:
        state.last_processed_id = latest.id
        state.save()


def new_user_creation():

    state = get_state("New User Creation")

    logs = Log.objects.filter(
        event_id=4720,
        id__gt=state.last_processed_id
    )

    if logs.exists():

       Alert.objects.get_or_create(
        rule_name="New User Creation",
        description="New user created",
        defaults={"severity": "Medium"}
)

    latest = Log.objects.order_by("-id").first()

    if latest:
        state.last_processed_id = latest.id
        state.save()