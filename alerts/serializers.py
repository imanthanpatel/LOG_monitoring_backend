
from rest_framework import serializers
from alerts.models import Alert
from detection.serializers import MitreTechniqueSerializer


class AlertSerializer(serializers.ModelSerializer):
    mitre_technique = MitreTechniqueSerializer()
    assigned_to = serializers.SerializerMethodField()
    investigation = serializers.SerializerMethodField()

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
            "assigned_to",
            "investigation",
            "timestamp",
        ]

    def get_assigned_to(self, obj):
        if not hasattr(obj, "investigation") or not obj.investigation.investigator:
            return None
        investigator = obj.investigation.investigator
        return {
            "id": investigator.id,
            "username": investigator.username,
            "email": investigator.email,
        }

    def get_investigation(self, obj):
        if not hasattr(obj, "investigation"):
            return None
        return obj.investigation.id



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