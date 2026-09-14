from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from investigations.models import Investigation
from evidence.models import Evidence
from evidence.serializers import EvidenceSerializer

from audit.utils import create_audit_log


class InvestigationEvidenceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        investigation = get_object_or_404(
            Investigation,
            id=id
        )

        # Only the assigned investigator can access
        if investigation.investigator != request.user:

            return Response(
                {
                    "error": "You are not assigned to this investigation."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        evidence = Evidence.objects.filter(
            investigation=investigation
        ).order_by("-uploaded_at")

        serializer = EvidenceSerializer(
            evidence,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request, id):

        investigation = get_object_or_404(
            Investigation,
            id=id
        )

        # Only assigned investigator can upload
        if investigation.investigator != request.user:

            return Response(
                {
                    "error": "You are not assigned to this investigation."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EvidenceSerializer(
            data=request.data
        )

        if serializer.is_valid():

            evidence = serializer.save(
                investigation=investigation,
                uploaded_by=request.user
            )

            # Create audit log
            create_audit_log(
                user=request.user,
                action="EVIDENCE_UPLOADED",
                description=(
                    f"Evidence #{evidence.id} uploaded to "
                    f"Investigation #{investigation.id} by "
                    f"{request.user.username}"
                ),
                alert_id=investigation.alert.id,
                investigation_id=investigation.id,
                evidence_id=evidence.id,
                ip_address=request.META.get("REMOTE_ADDR")
            )

            return Response(
                {
                    "message": "Evidence uploaded successfully.",
                    "evidence": EvidenceSerializer(
                        evidence,
                        context={"request": request}
                    ).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )