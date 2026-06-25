from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from ingestion.models import Log
from ingestion.serializers import LogSerializer
from django.utils.dateparse import parse_datetime
from django.utils import timezone

# Create your views here.
class LogListView(ListAPIView):
    queryset = Log.objects.all().order_by("-timestamp")
    serializer_class = LogSerializer



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
    



