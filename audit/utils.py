from audit.models import AuditLog


def create_audit_log(
    user,
    action,
    description,
    alert_id=None,
    investigation_id=None,
    evidence_id=None,
    ip_address=None
):

    return AuditLog.objects.create(
        user=user,
        action=action,
        description=description,
        alert_id=alert_id,
        investigation_id=investigation_id,
        evidence_id=evidence_id,
        ip_address=ip_address
    )


from .models import AuditLog


def create_audit_log(
    user=None,
    action=None,
    description="",
    alert_id=None,
    investigation_id=None,
    ip_address=None
):

    return AuditLog.objects.create(
        user=user,
        action=action,
        description=description,
        alert_id=alert_id,
        investigation_id=investigation_id,
        ip_address=ip_address
    )