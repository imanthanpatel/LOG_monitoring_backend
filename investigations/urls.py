from django.urls import path

from .views import (
    MyInvestigationListView,
    CompletedInvestigationListView,
    InvestigationDetailView,
    CompleteInvestigationView,
)

urlpatterns = [

    path(
        "investigations/me/",
        MyInvestigationListView.as_view(),
        name="my-investigations"
    ),

    path(
        "investigations/completed/",
        CompletedInvestigationListView.as_view(),
        name="completed-investigations"
    ),

    path(
        "investigations/<int:id>/",
        InvestigationDetailView.as_view(),
        name="investigation-detail"
    ),

    path(
        "investigations/<int:id>/complete/",
        CompleteInvestigationView.as_view(),
        name="investigation-complete"
    ),
]