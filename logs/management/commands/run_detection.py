import time
from django.core.management.base import BaseCommand

from logs.detection import (
    detect_bruteforce,
    detect_bruteforce_success,
    new_user_creation,
    powershell_execution,
    suspicious_powershell,
    service_installation,
    rdp_login,
    deleting_user,
    scheduled_task_created,
    suspicious_process,
    off_hours_login,
)


class Command(BaseCommand):
    help = "Real-Time SIEM Detection Engine"

    POLL_INTERVAL = 5  # seconds

    RULES = [
        ("Brute Force Detection", detect_bruteforce),
        ("Brute Force Success", detect_bruteforce_success),
        ("New User Creation", new_user_creation),
        ("User Deleted", deleting_user),
        ("PowerShell Execution", powershell_execution),
        ("Suspicious PowerShell", suspicious_powershell),
        ("Suspicious Process", suspicious_process),
        ("Scheduled Task Created", scheduled_task_created),
        ("RDP Login", rdp_login),
        ("Service Installation", service_installation),
        ("Off Hours Login", off_hours_login),
    ]

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS(
            "\n" + "=" * 60
        ))
        self.stdout.write(self.style.SUCCESS(
            "      SIEM REAL-TIME DETECTION ENGINE"
        ))
        self.stdout.write(self.style.SUCCESS(
            "=" * 60
        ))
        self.stdout.write(self.style.SUCCESS(
            f" Loaded {len(self.RULES)} Detection Rules"
        ))
        self.stdout.write(self.style.SUCCESS(
            f" Poll Interval: {self.POLL_INTERVAL} seconds"
        ))
        self.stdout.write(self.style.SUCCESS(
            "=" * 60 + "\n"
        ))

        cycle = 0

        try:

            while True:

                cycle += 1

                self.stdout.write(
                    self.style.NOTICE(
                        f"\n[Cycle {cycle}] "
                        f"{time.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                )

                success_count = 0
                fail_count = 0

                for rule_name, rule_function in self.RULES:

                    try:
                        rule_function()

                        success_count += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"  [OK] {rule_name}"
                            )
                        )

                    except Exception as e:

                        fail_count += 1

                        self.stdout.write(
                            self.style.ERROR(
                                f"  [FAIL] {rule_name}: {e}"
                            )
                        )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"[Cycle {cycle}] "
                        f"Completed | Success={success_count} "
                        f"Failed={fail_count}"
                    )
                )

                time.sleep(self.POLL_INTERVAL)

        except KeyboardInterrupt:

            self.stdout.write(
                self.style.WARNING(
                    "\n\n[*] Detection Engine stopped by user."
                )
            )

        except Exception as e:

            self.stdout.write(
                self.style.ERROR(
                    f"\n[CRITICAL ERROR] {e}"
                )
            )