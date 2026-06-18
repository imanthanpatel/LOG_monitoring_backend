from django.db import models

class Log(models.Model):
    event_id = models.IntegerField()
    source = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_id}"

class Alert(models.Model):
    rule_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rule_name