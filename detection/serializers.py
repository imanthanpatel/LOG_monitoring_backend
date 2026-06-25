from rest_framework import serializers
from detection.models import RuleConfig,MitreTechnique


class RuleConfigSerializer(serializers.ModelSerializer):

    mitre_id = serializers.CharField(
        source="mitre.technique_id",
        read_only=True
    )

    mitre_name = serializers.CharField(
        source="mitre.name",
        read_only=True
    )

    class Meta:
        model = RuleConfig
        fields = [
            "id",
            "name",
            "severity",
            "enabled",
            "mitre",
            "mitre_id",
            "mitre_name",
        ]


class MitreTechniqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = MitreTechnique
        fields = "__all__"