from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from audit.models import AuditLog
from audit.serializers import AuditLogSerializer


class AuditLogListView(ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = AuditLog.objects.all()

    serializer_class = AuditLogSerializer