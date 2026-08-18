from rest_framework import serializers

from investigations.models import Investigation
from evidence.serializers import EvidenceSerializer


class InvestigationSerializer(serializers.ModelSerializer):

    evidence = EvidenceSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Investigation

        fields = [
            "id",
            "status",
            "summary",
            "root_cause",
            "recommendations",
            "conclusion",
            "evidence",
            "created_at",
            "updated_at",
            "completed_at",
            "alert",
            "assigned_by",
            "investigator",
        ]


class InvestigationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investigation

        fields = [
            "status",
            "summary",
            "root_cause",
            "recommendations",
            "conclusion",
        ]