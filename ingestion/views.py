from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from ingestion.models import Log
from ingestion.serializers import LogSerializer
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

# Create your views here.

#logic of /api/logs 
class LogListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogSerializer
    ALLOWED_ORDERING = (
        "time_generated",
        "-time_generated",
        "event_id",
        "-event_id",
    )


    def get_queryset(self):
        queryset = Log.objects.all()
        # queryset = Log.objects.all().order_by("-time_genrated")
        # queryset = Log.objects.all().order_by("-time_generated")
        #instead of hardcoding i'd like to do 
        ordering = self.request.query_params.get("ordering")
        event_id = self.request.query_params.get("event_id")
        source = self.request.query_params.get("source")
        log_type = self.request.query_params.get("log_type")
        username = self.request.query_params.get("username")
        computer = self.request.query_params.get("computer")
        ip_address = self.request.query_params.get("ip_address")

        if event_id:
            queryset = queryset.filter(event_id=event_id)

        if source:
            queryset = queryset.filter(source=source)

        if log_type:
            queryset = queryset.filter(log_type=log_type)

        if username:
            queryset = queryset.filter(username__icontains=username)

        if computer:
            queryset = queryset.filter(computer__icontains=computer)

        if ip_address:
            queryset = queryset.filter(ip_address=ip_address)
       
       
        if ordering in self.ALLOWED_ORDERING:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-time_generated")
                
       

        return queryset
          
        
            
      


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
    



