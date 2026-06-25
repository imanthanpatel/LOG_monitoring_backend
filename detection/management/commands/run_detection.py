from django.core.management.base import BaseCommand
from detection.engine import run_all_rules
import time


class Command(BaseCommand):
    help = "Run Detection Engine"

    def handle(self, *args, **kwargs):
        self.stdout.write("Detection Engine Started")

        while True:
            run_all_rules()
            time.sleep(5)