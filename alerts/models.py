from django.db import models
from detection.models import MitreTechnique


class Alert(models.Model):

    SEVERITY_CHOICES = [
        ("Critical", "Critical"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("ASSIGNED", "Assigned"),
        ("FALSE_POSITIVE", "False Positive"),
        ("RESOLVED", "Resolved"),
        ("CLOSED", "Closed"),
    ]

    rule_name = models.CharField(
        max_length=100
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES
    )

    description = models.TextField()

    mitre_technique = models.ForeignKey(
        MitreTechnique,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    assigned = models.BooleanField(
        default=False
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.rule_name} ({self.severity})"