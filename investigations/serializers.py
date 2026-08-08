from rest_framework import serializers
from investigations.models import Investigation


from rest_framework import serializers
from investigations.models import Investigation


class InvestigationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investigation
        fields = "__all__"

class InvestigationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investigation
        fields = [
            "status",
            "summary",
            "root_cause",
            "recommendations",
            "conclusion",
            "evidence",
        ]