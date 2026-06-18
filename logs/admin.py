from django.contrib import admin

# Register your models here.
from .models import Log, Alert

admin.site.register(Log)
admin.site.register(Alert)