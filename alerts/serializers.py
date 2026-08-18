
from rest_framework import serializers
from alerts.models import Alert
from detection.serializers import MitreTechniqueSerializer


class AlertSerializer(serializers.ModelSerializer):
    mitre_technique = MitreTechniqueSerializer()

    class Meta:
        model = Alert
        fields = [
            "id",
            "mitre_technique",
            "rule_name",
            "severity",
            "description",
            "status",
            "assigned",
            "timestamp",
        ]

    def get_assigned(self, obj):
        return hasattr(obj, "investigation")



class AlertStatusSerializer(serializers.Serializer):

    id = serializers.IntegerField()

    status = serializers.ChoiceField(
        choices=[
            ("OPEN", "Open"),
            ("ASSIGNED", "Assigned"),
            ("FALSE_POSITIVE", "False Positive"),
            ("RESOLVED", "Resolved"),
        ]
    )
class AlertAssignSerializer(serializers.Serializer):

    investigator = serializers.IntegerField()


# class IncidentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Incident
#         fields = "__all__"