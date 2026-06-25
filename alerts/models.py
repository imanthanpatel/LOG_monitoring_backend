from django.db import models

from detection.models import MitreTechnique


# Create your models 
class Alert(models.Model):

    SEVERITY_CHOICES = [
        ("Critical", "Critical"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
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

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.rule_name} ({self.severity})"
    




class Incident(models.Model):

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("Investigating", "Investigating"),
        ("Resolved", "Resolved"),
        ("Closed", "Closed"),
    ]

    alert = models.ForeignKey(
        Alert,
        on_delete=models.CASCADE,
        related_name="incidents"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    assigned_to = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Incident #{self.id} - {self.alert.rule_name}"
