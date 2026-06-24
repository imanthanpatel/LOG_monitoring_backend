from django.urls import path
from .views import LogListView,AlertListView,DashboardView,statsView,LogIngestView,IncidentListView

urlpatterns = [
    path("ingest/", LogIngestView.as_view()),
    path("logs/list/", LogListView.as_view()),
    path("alerts/", AlertListView.as_view()),
    path("dashboard/", DashboardView.as_view()),
    path("stats/", statsView),
    path( "incidents/",IncidentListView.as_view()),
]