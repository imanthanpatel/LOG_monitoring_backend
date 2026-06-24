from django.db import models


class Log(models.Model):

    event_id = models.IntegerField(db_index=True)

    source = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    log_type = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    message = models.TextField(
        null=True,
        blank=True
    )

    keyword = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    computer = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    username = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    ip_address = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    time_generated = models.DateTimeField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.event_id} - {self.source}"


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

    mitre_technique = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.rule_name} ({self.severity})"


class DetectionState(models.Model):

    rule_name = models.CharField(
        max_length=100,
        unique=True
    )

    last_processed_id = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.rule_name


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