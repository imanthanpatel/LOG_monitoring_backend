from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication

from alerts.models import Alert
from alerts.serializers import (
    AlertSerializer,
    AlertAssignSerializer
)

from ingestion.models import Log
from detection.models import RuleConfig
from investigations.models import Investigation

from audit.utils import create_audit_log


# ==========================================
# DASHBOARD
# ==========================================

class DashboardView(APIView):

    def get(self, request):

        return Response({
            "total_logs": Log.objects.count(),
            "total_alerts": Alert.objects.count(),

            "active_rules": RuleConfig.objects.filter(
                enabled=True
            ).count(),

            "critical_alerts": Alert.objects.filter(
                severity="Critical"
            ).count(),

            "high_alerts": Alert.objects.filter(
                severity="High"
            ).count(),

            "medium_alerts": Alert.objects.filter(
                severity="Medium"
            ).count(),

            "low_alerts": Alert.objects.filter(
                severity="Low"
            ).count(),

            "total_users": User.objects.count(),

            "failed_logins": Log.objects.filter(
                event_id=4625
            ).count(),
        })


# ==========================================
# ALERT STATISTICS
# ==========================================

@api_view(["GET"])
def statsView(request):

    return Response({
        "total_logs": Log.objects.count(),

        "total_alerts": Alert.objects.count(),

        "critical": Alert.objects.filter(
            severity="Critical"
        ).count(),

        "high": Alert.objects.filter(
            severity="High"
        ).count(),

        "medium": Alert.objects.filter(
            severity="Medium"
        ).count(),

        "low": Alert.objects.filter(
            severity="Low"
        ).count(),
    })


# ==========================================
# LIST ALL ALERTS
# ==========================================

class AlertListView(ListAPIView):

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


# ==========================================
# GET SINGLE ALERT
# ==========================================

class AlertDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        alert = get_object_or_404(
            Alert,
            id=id
        )

        serializer = AlertSerializer(alert)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# ==========================================
# UPDATE ALERT STATUS
# ==========================================

class AlertStatusView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):

        alert_id = request.data.get("id")
        new_status = request.data.get("status")

        alert = get_object_or_404(
            Alert,
            id=alert_id
        )

        alert.status = new_status
        alert.save()

        serializer = AlertSerializer(alert)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# ==========================================
# ASSIGN ALERT TO INVESTIGATOR
# ==========================================

class AlertAssignView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        # ----------------------------------
        # 1. Get Alert
        # ----------------------------------

        alert = get_object_or_404(
            Alert,
            id=id
        )

        # ----------------------------------
        # 2. Check if alert is already assigned
        # ----------------------------------

        if Investigation.objects.filter(
            alert=alert
        ).exists():

            return Response(
                {
                    "error": "Alert is already assigned."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ----------------------------------
        # 3. Validate request data
        # ----------------------------------

        serializer = AlertAssignSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        investigator_id = serializer.validated_data[
            "investigator"
        ]

        # ----------------------------------
        # 4. Get Investigator
        # ----------------------------------

        investigator = get_object_or_404(
            User,
            id=investigator_id
        )

        # ----------------------------------
        # 5. Check investigator role
        # ----------------------------------

        if investigator.profile.role != "INVESTIGATOR":

            return Response(
                {
                    "error": (
                        "Selected user is not an investigator."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ----------------------------------
        # 6. Create Investigation
        # ----------------------------------

        investigation = Investigation.objects.create(
            alert=alert,
            investigator=investigator,
            assigned_by=request.user,
            status="ASSIGNED"
        )

        # ----------------------------------
        # 7. Update Alert
        # ----------------------------------

        alert.status = "ASSIGNED"
        alert.assigned = True
        alert.save()

        # ----------------------------------
        # 8. Create Audit Log
        # ----------------------------------

        create_audit_log(
            user=request.user,
            action="ALERT_ASSIGNED",
            description=(
                f"Alert #{alert.id} assigned to "
                f"{investigator.username}"
            ),
            alert_id=alert.id,
            investigation_id=investigation.id,
            ip_address=request.META.get(
                "REMOTE_ADDR"
            )
        )

        # ----------------------------------
        # 9. Return Response
        # ----------------------------------

        return Response(
            {
                "message": (
                    "Alert assigned successfully."
                ),

                "alert_id": alert.id,

                "investigator": investigator.username,

                "investigation_id": investigation.id,

                "alert_status": alert.status,

                "investigation_status": (
                    investigation.status
                )
            },
            status=status.HTTP_201_CREATED
        )