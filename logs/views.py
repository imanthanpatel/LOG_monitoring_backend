from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Log,Alert
from .serializers import LogSerializer,AlertSerializer
from .pagination import LogPagination




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
    
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Log, Alert

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