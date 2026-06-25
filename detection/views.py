from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from detection.models import RuleConfig, MitreTechnique
from detection.serializers import (
    RuleConfigSerializer,
    MitreTechniqueSerializer,
)


class RuleConfigViewSet(viewsets.ModelViewSet):

    queryset = RuleConfig.objects.all()
    serializer_class = RuleConfigSerializer

    @action(detail=False,methods=["get"])
    def stats(self, request):

        return Response({
            "total_rules": RuleConfig.objects.count(),
            "enabled_rules": RuleConfig.objects.filter(
                enabled=True
            ).count(),
            "disabled_rules": RuleConfig.objects.filter(
                enabled=False
            ).count(),
        })


class MitreTechniqueViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = MitreTechnique.objects.all()
    serializer_class = MitreTechniqueSerializer

    @action(detail=False,methods=["get"])
    def stats(self, request):

        total_techniques = MitreTechnique.objects.count()

        total_tactics = (
            MitreTechnique.objects
            .exclude(tactic__isnull=True)
            .values("tactic")
            .distinct()
            .count()
        )

        return Response({
            "total_techniques": total_techniques,
            "total_tactics": total_tactics,
        })

    @action(detail=False,methods=["get"])
    def coverage(self, request):

        mapped_rules = RuleConfig.objects.filter(
            mitre__isnull=False
        ).count()

        total_rules = RuleConfig.objects.count()

        coverage = 0

        if total_rules:
            coverage = round(
                (mapped_rules / total_rules) * 100,
                2
            )

        return Response({
            "total_rules": total_rules,
            "mapped_rules": mapped_rules,
            "coverage_percent": coverage,
        })