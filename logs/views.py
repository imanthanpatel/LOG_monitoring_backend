from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Log,Alert,Incident
from .serializers import LogSerializer,AlertSerializer,IncidentSerializer
from .pagination import LogPagination,IncidentPagination
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Log, Alert,Incident






class LogListView(ListAPIView):
    queryset = Log.objects.all().order_by("-timestamp")
    serializer_class = LogSerializer
    pagination_class = LogPagination

class AlertListView(ListAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class DashboardView(APIView):
    def get(self, request):
        return Response({
            "total_logs": Log.objects.count(),
            "total_alerts": Alert.objects.count(),
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





class LogIngestView(APIView):

    def post(self, request):

        time_generated = parse_datetime(
         request.data.get("time_generated")
    )

        if time_generated and timezone.is_naive(time_generated):
            time_generated = timezone.make_aware(
            time_generated,
            timezone.get_current_timezone()
    )

        Log.objects.create(
            event_id=request.data.get("event_id"),
            source=request.data.get("source"),
            log_type=request.data.get("log_type"),
            message=request.data.get("message"),
            computer=request.data.get("computer"),
            ip_address=request.data.get("ip_address"),
            username=request.data.get("username"),
            time_generated=time_generated
        )

        return Response(
            {"status": "success"},
            status=201
        )

        # return Response({"status":"received"})



class IncidentListView(ListAPIView):
    queryset = Incident.objects.all().order_by("-created_at")
    serializer_class = IncidentSerializer
    pagination_class= IncidentPagination