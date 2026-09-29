from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):

    TYPE_CHOICES = [
        ("ALERT_ASSIGNED", "Alert Assigned"),
        ("INVESTIGATION_COMPLETED", "Investigation Completed"),
        ("ALERT_CLOSED", "Alert Closed"),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    alert_id = models.IntegerField(
        null=True,
        blank=True
    )

    investigation_id = models.IntegerField(
        null=True,
        blank=True
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"