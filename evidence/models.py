from django.db import models
from django.contrib.auth.models import User

from investigations.models import Investigation

# Create your models here.
class Evidence(models.Model):

    investigation = models.ForeignKey(
        Investigation,
        on_delete=models.CASCADE,
        related_name="evidence"
    )

    file = models.FileField(
        upload_to="investigations/evidence/"
    )

    description = models.TextField(
        blank=True
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_evidence"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Evidence #{self.id} - Investigation #{self.investigation.id}"