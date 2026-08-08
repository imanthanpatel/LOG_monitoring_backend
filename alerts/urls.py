from django.urls import path

from .views import (
    AlertListView,
    DashboardView,
    statsView,
    AlertDetailView,
    AlertStatusView,
    AlertAssignView,
)

urlpatterns = [
    path("alerts/", AlertListView.as_view()),

    path(
        "alerts/<int:id>/",
        AlertDetailView.as_view()
    ),

    path(
        "alerts/status/",
        AlertStatusView.as_view()
    ),

    path(
        "alerts/<int:id>/assign/",
        AlertAssignView.as_view()
    ),

    path(
        "dashboard/",
        DashboardView.as_view()
    ),

    path(
        "stats/",
        statsView
    ),
]