from django.urls import path
from evidence.views import InvestigationEvidenceView

urlpatterns = [
    path(
        "investigations/<int:id>/evidence/",
        InvestigationEvidenceView.as_view(),
        name="investigation-evidence"
    ),
]