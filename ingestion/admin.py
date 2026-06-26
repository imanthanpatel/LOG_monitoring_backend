from django.contrib import admin
from ingestion.models import Log, DetectionState

admin.site.register(Log)
admin.site.register(DetectionState)