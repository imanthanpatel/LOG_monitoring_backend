from django.urls import path
from .views import (
    AlertListView,
    IncidentListView,
    DashboardView,
    statsView
)

urlpatterns = [
    path("alerts/", AlertListView.as_view()),
    path("incidents/", IncidentListView.as_view()),
    path("dashboard/", DashboardView.as_view()),
    path("stats/", statsView),
]