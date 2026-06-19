from celery import shared_task
from logs.detection import detect_bruteforce, new_user_creation, powershell_execution

@shared_task
def run_detection_engine():
    detect_bruteforce()
    new_user_creation()
    powershell_execution()