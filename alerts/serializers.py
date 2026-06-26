
from rest_framework import serializers
from alerts.models import Alert, Incident
from detection.serializers import MitreTechniqueSerializer


class AlertSerializer(serializers.ModelSerializer):
    mitre_technique = MitreTechniqueSerializer()

    class Meta:
        model = Alert
        fields = '__all__'


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"