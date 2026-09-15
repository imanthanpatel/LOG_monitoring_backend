from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class MyNotificationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by("-created_at")


class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        notification = get_object_or_404(
            Notification,
            id=id,
            recipient=request.user
        )

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response(
            {
                "message": "Notification marked as read.",
                "notification_id": notification.id,
                "is_read": notification.is_read
            },
            status=status.HTTP_200_OK
        )