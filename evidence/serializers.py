from rest_framework import serializers

from evidence.models import Evidence


class EvidenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evidence
        fields = [
            "id",
            "investigation",
            "file",
            "description",
            "uploaded_by",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "investigation",
            "uploaded_by",
            "uploaded_at",
        ]