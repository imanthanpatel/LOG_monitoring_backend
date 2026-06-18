from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Log,Alert
from .serializers import LogSerializer,AlertSerializer




class LogListView(ListAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

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