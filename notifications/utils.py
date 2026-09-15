from notifications.models import Notification


def create_notification(
    recipient,
    notification_type,
    title,
    message,
    alert_id=None,
    investigation_id=None
):
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        alert_id=alert_id,
        investigation_id=investigation_id
    )