from django.db import models
from django.contrib.auth.models import User
from alerts.models import Alert
# from evidence.models import evidence


class Investigation(models.Model):

    STATUS_CHOICES = [
        # ("NOT_ASSIGNED", "Not Assigned"),
        ("ASSIGNED", "Assigned"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CLOSED", "Closed"),
    ]

    alert = models.OneToOneField(
        Alert,
        on_delete=models.CASCADE,
        related_name="investigation"
    )

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_investigations"
    )

    investigator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="investigations"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ASSIGNED"
    )
    # file = models.FileField(
    #     upload_to="investigations/evidence/",
    #     null=True,
    #     blank=True
    # )

    summary = models.TextField(blank=True)

    root_cause = models.TextField(blank=True)

    recommendations = models.TextField(blank=True)

    conclusion = models.TextField(blank=True)

    # evidence = models.FileField(
    #     upload_to="investigation_upload/",
    #     blank=True,
    #     null=True,
    # )
    # evidence = models.ForeignKey(
    #    evidence,
    #    on_delete=models.SET_NULL,
    #    null=True,
    #    blank=True
    # )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Investigation #{self.id} - Alert {self.alert.id}"