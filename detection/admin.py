from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import RuleConfig, MitreTechnique


@admin.register(RuleConfig)
class RuleConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "severity",
        "enabled",
        "mitre",
    )

    list_filter = (
        "enabled",
        "severity",
    )


@admin.register(MitreTechnique)
class MitreTechniqueAdmin(admin.ModelAdmin):
    list_display = (
        "technique_id",
        "name",
        "tactic",
    )