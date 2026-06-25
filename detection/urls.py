from django.urls import path, include
from rest_framework.routers import DefaultRouter

from detection.views import (
    RuleConfigViewSet,
    # RuleStatsView,
    MitreTechniqueViewSet,
)

router = DefaultRouter()

router.register(
    r"rules",
    RuleConfigViewSet,
    basename="rules"
)

router.register(
    r"mitre",
    MitreTechniqueViewSet,
    basename="mitre"
)

urlpatterns = [



    path(
        "mitre/coverage/",
        MitreTechniqueViewSet.as_view({"get": "coverage"}),
        name="mitre-coverage"
    ),

    path(
        "mitre/stats/",
        MitreTechniqueViewSet.as_view({"get": "stats"}),
        name="mitre-stats"
    ),

    path("", include(router.urls)),

]