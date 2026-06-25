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

