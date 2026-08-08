from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from alerts.models import Alert
from alerts.serializers import AlertSerializer,AlertAssignSerializer,AlertStatusSerializer
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ingestion.models import Log
from detection.models import RuleConfig
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from investigations.models import Investigation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status



 



# Create your views here.
# class IncidentListView(ListAPIView):
#     queryset = Incident.objects.all().order_by("-created_at")
#     serializer_class = IncidentSerializer

class DashboardView(APIView):
    def get(self, request):
        print("Reached Dashboard View")
        return Response({
            "total_logs": Log.objects.count(),
            "total_alerts": Alert.objects.count(),
            "active_rules": RuleConfig.objects.filter(enabled=True).count(),
            # "total_incidents": Incident.objects.count(),
            "critical_alerts": Alert.objects.filter(severity="Critical").count(),
            "high_alerts": Alert.objects.filter(severity="High").count(),
            "medium_alerts": Alert.objects.filter(severity="Medium").count(),
            "low_alerts": Alert.objects.filter(severity="Low").count(),
            "total_users": User.objects.count(),
            "failed_logins": Log.objects.filter(event_id=4625).count(),
        })
    


@api_view(['GET'])
def statsView(request):
    return Response({
        "total_logs": Log.objects.count(),
        "total_alerts": Alert.objects.count(),
        "critical": Alert.objects.filter(severity="Critical").count(),
        "high": Alert.objects.filter(severity="High").count(),
        "medium": Alert.objects.filter(severity="Medium").count(),
        "low": Alert.objects.filter(severity="Low").count(),
    })





class AlertListView(ListAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class AlertDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        alert = get_object_or_404(Alert, id=id)
        serializer = AlertSerializer(alert)
        return Response(serializer.data)
    
class AlertStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):

        alert_id = request.data.get("id")
        new_status = request.data.get("status")

        alert = get_object_or_404(Alert, id=alert_id)

        alert.status = new_status
        alert.save()

        serializer = AlertSerializer(alert)

        return Response(serializer.data)

class AlertAssignView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        # 1. Get alert from URL
        alert = get_object_or_404(Alert, id=id)

        # 2. Validate request body
        serializer = AlertAssignSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        investigator_id = serializer.validated_data["investigator"]

        # 3. Check if alert is already assigned
        if Investigation.objects.filter(alert=alert).exists():
            return Response(
                {
                    "error": "Alert is already assigned."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Find investigator
        investigator = get_object_or_404(
            User,
            id=investigator_id
        )

        # 5. Check investigator role
        if investigator.profile.role != "INVESTIGATOR":
            return Response(
                {
                    "error": "Selected user is not an investigator."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 6. Create investigation
        investigation = Investigation.objects.create(
            alert=alert,
            investigator=investigator,
            assigned_by=request.user,
            status="ASSIGNED"
        )

        # 7. Update alert status
        alert.status = "ASSIGNED"
        alert.save()

        # 8. Return response
        return Response(
            {
                "message": "Alert assigned successfully.",
                "alert_id": alert.id,
                "investigator": investigator.username,
                "investigation_id": investigation.id,
                "status": investigation.status
            },
            status=status.HTTP_201_CREATED
        )
        