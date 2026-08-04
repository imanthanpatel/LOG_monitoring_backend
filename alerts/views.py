from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from alerts.models import Alert, Incident
from alerts.serializers import AlertSerializer, IncidentSerializer
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ingestion.models import Log
from detection.models import RuleConfig
from django.contrib.auth.models import User
 



# Create your views here.
class IncidentListView(ListAPIView):
    queryset = Incident.objects.all().order_by("-created_at")
    serializer_class = IncidentSerializer

class DashboardView(APIView):
    def get(self, request):
        print("Reached Dashboard View")
        return Response({
            "total_logs": Log.objects.count(),
            "total_alerts": Alert.objects.count(),
            "active_rules": RuleConfig.objects.filter(enabled=True).count(),
            "total_incidents": Incident.objects.count(),
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