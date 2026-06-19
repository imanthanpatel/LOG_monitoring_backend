import time
from django.core.management.base import BaseCommand
from logs.detection import detect_bruteforce, new_user_creation, powershell_execution


class Command(BaseCommand):
    help = "Real-time log detection engine"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting SIEM engine...")

        while True:
            try:
                detect_bruteforce()
                new_user_creation()
                powershell_execution()

                self.stdout.write("Checked logs...")

                time.sleep(5)  # runs every 5 seconds

            except KeyboardInterrupt:
                self.stdout.write("Stopping SIEM engine...")
                break