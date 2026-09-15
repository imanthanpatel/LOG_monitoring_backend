from django.urls import path
from notifications.views import (
    MyNotificationListView,
    NotificationMarkReadView
)

urlpatterns = [
    path(
        "notifications/",
        MyNotificationListView.as_view(),
        name="my-notifications"
    ),

    path(
        "notifications/<int:id>/read/",
        NotificationMarkReadView.as_view(),
        name="notification-mark-read"
    ),
]