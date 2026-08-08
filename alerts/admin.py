from django.contrib import admin
from alerts.models import Alert


# Register your models here.
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("rule_name", "severity", "timestamp")
    list_filter = ("severity", "timestamp")
    search_fields = ("rule_name", "description")


# @admin.register(Incident)
# class IncidentAdmin(admin.ModelAdmin):
#     list_display = ("alert", "status", "assigned_to", "created_at", "updated_at")
#     list_filter = ("status", "created_at", "updated_at")    