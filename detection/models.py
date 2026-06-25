from django.db import models


class MitreTechnique(models.Model):

    technique_id = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(max_length=255)

    tactic = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.technique_id} - {self.name}"


class RuleConfig(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    severity = models.CharField(
        max_length=20,
        default="Low"
    )

    enabled = models.BooleanField(
        default=True
    )

    mitre = models.ForeignKey(
        'MitreTechnique',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name