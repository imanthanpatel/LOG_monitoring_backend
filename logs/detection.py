from django.utils import timezone
from datetime import timedelta
from .models import Log, Alert


def detect_bruteforce():
    time_threshold = timezone.now() - timedelta(minutes=5)

    failed = Log.objects.filter(
        event_id=4625,
        timestamp__gte=time_threshold   # assuming you have timestamp field
    ).count()

    if failed > 5:
        Alert.objects.create(
            rule_name="Brute Force",
            severity="High",
            description="More than 5 failed logins in 5 minutes"
        )


def powershell_execution():
    # exe = Log.objects.filter(source="powershell.exe")
    time_threshold = timezone.now() - timedelta(seconds=30)
    exe = Log.objects.filter(
        source="powershell.exe",
        timestamp__gte=time_threshold
    )
    

    if exe.exists():
        Alert.objects.create(
            rule_name="PowerShell execution",
            severity="High",
            description="PowerShell execution detected"
        )


def new_user_creation():
    new_users = Log.objects.filter(event_id=4720)
    time_threshold = timezone.now() - timedelta(seconds=30)
    new_users = Log.objects.filter(
        event_id=4720,
        timestamp__gte=time_threshold
    )


    if new_users.exists():
        Alert.objects.create(
            rule_name="New User Creation",
            severity="Medium",
            description="New user created recently"
        )