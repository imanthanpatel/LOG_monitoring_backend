from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ("ALERT_ASSIGNED", "Alert Assigned"),
        ("INVESTIGATION_UPDATED", "Investigation Updated"),
        ("EVIDENCE_UPLOADED", "Evidence Uploaded"),
        ("INVESTIGATION_COMPLETED", "Investigation Completed"),
        ("ALERT_CLOSED", "Alert Closed"),
        ("USER_LOGIN", "User Login"),
        ("USER_LOGOUT", "User Logout"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs"
    )

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    alert_id = models.IntegerField(
        null=True,
        blank=True
    )

    investigation_id = models.IntegerField(
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        username = self.user.username if self.user else "System"

        return (
            f"{username} - {self.action} - "
            f"{self.created_at}"
        )