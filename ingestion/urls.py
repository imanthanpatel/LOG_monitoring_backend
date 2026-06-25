from django.urls import path
from .views import LogListView, LogIngestView

urlpatterns = [
    path("ingest/", LogIngestView.as_view()),
    path("logs/", LogListView.as_view()),
]