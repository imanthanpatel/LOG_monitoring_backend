from django.db import transaction
from django.db.models import Q
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
from accounts.permissions import IsInvestigator, IsAdminOrSOC
from audit.utils import create_audit_log
from notifications.utils import create_notification


class MyInvestigationListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsInvestigator]
    serializer_class = InvestigationSerializer

    def get_queryset(self):
        return Investigation.objects.filter(
            investigator=self.request.user
        ).order_by("-created_at")


class CompletedInvestigationListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSOC]
    serializer_class = InvestigationSerializer

    def get_queryset(self):
        return Investigation.objects.filter(
            Q(status__iexact="COMPLETED") | Q(status__iexact="CLOSED")
        ).select_related(
            "alert", "investigator", "assigned_by"
        ).order_by("-completed_at", "-updated_at")


class InvestigationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        investigation = get_object_or_404(
            Investigation,
            id=id
        )

        is_owner = investigation.investigator == request.user
        is_soc_or_admin = request.user.profile.role in ["SOC", "ADMIN"]
        if not is_owner and not is_soc_or_admin:
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

    @transaction.atomic
    def post(self, request, id):

        investigation = get_object_or_404(
            Investigation,
            id=id
        )

        # =====================================
        # CHECK INVESTIGATOR
        # =====================================

        if investigation.investigator != request.user:
            return Response(
                {
                    "error": "You are not assigned to this investigation."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # =====================================
        # CHECK ALREADY COMPLETED
        # =====================================

        if investigation.status in ["COMPLETED", "CLOSED"]:
            return Response(
                {
                    "error": "Investigation is already completed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =====================================
        # CHECK REQUIRED FIELDS
        # =====================================

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

        # =====================================
        # COMPLETE INVESTIGATION
        # =====================================

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

        # =====================================
        # AUDIT LOG - INVESTIGATION COMPLETED
        # =====================================

        create_audit_log(
            user=request.user,
            action="INVESTIGATION_COMPLETED",
            description=(
                f"Investigation #{investigation.id} completed by "
                f"{request.user.username}. "
                f"Alert #{alert.id} was closed."
            ),
            alert_id=alert.id,
            investigation_id=investigation.id,
            ip_address=request.META.get("REMOTE_ADDR")
        )

        # =====================================
        # AUDIT LOG - ALERT CLOSED
        # =====================================

        create_audit_log(
            user=request.user,
            action="ALERT_CLOSED",
            description=(
                f"Alert #{alert.id} closed after "
                f"Investigation #{investigation.id} was completed."
            ),
            alert_id=alert.id,
            investigation_id=investigation.id,
            ip_address=request.META.get("REMOTE_ADDR")
        )

        # =====================================
        # NOTIFY SOC
        # =====================================

        if investigation.assigned_by:
            create_notification(
                recipient=investigation.assigned_by,
                notification_type="INVESTIGATION_COMPLETED",
                title="Investigation Completed",
                message=(
                    f"Investigation #{investigation.id} has been "
                    f"completed by {request.user.username}. "
                    f"Alert #{alert.id} has been closed."
                ),
                alert_id=alert.id,
                investigation_id=investigation.id
            )

        # =====================================
        # SUCCESS RESPONSE
        # =====================================

        return Response(
            {
                "message": "Investigation completed successfully.",
                "investigation_id": investigation.id,
                "investigation_status": investigation.status,
                "alert_id": alert.id,
                "alert_status": alert.status,
                "completed_at": investigation.completed_at
            },
            status=status.HTTP_200_OK
        )