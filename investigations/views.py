from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from investigations.models import Investigation
from investigations.serializers import (
    InvestigationSerializer,
    InvestigationUpdateSerializer
)
from accounts.permissions import IsInvestigator
from audit.utils import create_audit_log


class MyInvestigationListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsInvestigator]
    serializer_class = InvestigationSerializer

    def get_queryset(self):
        return Investigation.objects.filter(
            investigator=self.request.user
        ).order_by("-created_at")


class InvestigationDetailView(APIView):
    permission_classes = [IsAuthenticated, IsInvestigator]

    def get(self, request, id):
        investigation = get_object_or_404(
            Investigation,
            id=id
        )

        # Investigator can only see their own investigation
        if investigation.investigator != request.user:
            return Response(
                {
                    "error": "You are not assigned to this investigation."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = InvestigationSerializer(investigation)

        return Response(serializer.data)

    def patch(self, request, id):

        investigation = get_object_or_404(
            Investigation,
            id=id
        )

        # Ownership check
        if investigation.investigator != request.user:
            return Response(
                {
                    "error": "You are not assigned to this investigation."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Don't allow modification after completion
        if investigation.status in ["COMPLETED", "CLOSED"]:
            return Response(
                {
                    "error": "Investigation is already completed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InvestigationUpdateSerializer(
            investigation,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

             # Create Audit Log
            create_audit_log(
                user=request.user,
                action="INVESTIGATION_UPDATED",
                description=(
                    f"Investigation #{investigation.id} "
                    f"was updated by {request.user.username}"
                ),
                alert_id=investigation.alert.id,
                investigation_id=investigation.id,
                ip_address=request.META.get("REMOTE_ADDR")
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CompleteInvestigationView(APIView):
    permission_classes = [IsAuthenticated, IsInvestigator]

    def post(self, request, id):

        investigation = get_object_or_404(
            Investigation,
            id=id
        )

        # Check investigator
        if investigation.investigator != request.user:
            return Response(
                {
                    "error": "You are not assigned to this investigation."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Already completed?
        if investigation.status in ["COMPLETED", "CLOSED"]:
            return Response(
                {
                    "error": "Investigation is already completed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Required investigation fields
        required_fields = {
            "summary": investigation.summary,
            "root_cause": investigation.root_cause,
            "recommendations": investigation.recommendations,
            "conclusion": investigation.conclusion,
        }

        missing_fields = [
            field
            for field, value in required_fields.items()
            if not value or not value.strip()
        ]

        if missing_fields:
            return Response(
                {
                    "error": "Complete all investigation fields before submitting.",
                    "missing_fields": missing_fields
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Complete investigation
        investigation.status = "COMPLETED"
        investigation.completed_at = timezone.now()
        investigation.save()

        # =====================================
        # CLOSE RELATED ALERT
        # =====================================

        alert = investigation.alert
        alert.status = "CLOSED"
        alert.assigned = True
        alert.save()

        return Response(
            {
                "message": "Investigation completed successfully.",
                "investigation_id": investigation.id,
                "status": investigation.status,
                "completed_at": investigation.completed_at
            },
            status=status.HTTP_200_OK
        )