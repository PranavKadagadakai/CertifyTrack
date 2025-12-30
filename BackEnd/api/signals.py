import hashlib

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (
    AICTEPointTransaction,
    AuditLog,
    Certificate,
    Notification,
    User,
)


@receiver(pre_save, sender=Certificate)
def prevent_certificate_file_change(sender, instance, **kwargs):
    """
    Prevent modification or removal of the certificate file once it exists.
    """
    if not instance.pk:
        return

    try:
        original = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    orig_has_file = bool(
        original.file and getattr(original.file, "name", None)
    )
    new_has_file = bool(instance.file and getattr(instance.file, "name", None))

    if orig_has_file and not new_has_file:
        raise ValidationError(
            "Certificate file cannot be removed once set (immutable)."
        )

    if (
        orig_has_file
        and new_has_file
        and original.file.name != instance.file.name
    ):
        raise ValidationError("Certificate file is immutable once set.")


@receiver(post_save, sender=Certificate)
def compute_certificate_hash(sender, instance, created, **kwargs):
    """
    Compute SHA256 hash of certificate file after it's saved and update file_hash.
    """
    try:
        if instance.file and (not instance.file_hash):
            try:
                with instance.file.open("rb") as f:
                    data = f.read()
            except Exception:
                return

            digest = hashlib.sha256(data).hexdigest()
            sender.objects.filter(pk=instance.pk).update(file_hash=digest)
    except Exception:
        return


@receiver(post_save, sender=AICTEPointTransaction)
def notify_on_transaction_status_change(sender, instance, created, **kwargs):
    """
    When an AICTE transaction is created or updated, notify the student of the status.
    Also create an audit log entry for traceability.
    """
    status = instance.status
    user = instance.student.user
    title = f"AICTE points {status.lower()}"
    message = f"Your AICTE points for event '{instance.event.name}' (category: {instance.category.name}) are now: {status}. Allocated points: {instance.points_allocated}."

    Notification.objects.create(user=user, title=title, message=message)
    AuditLog.objects.create(
        user=user, action=f"AICTE transaction {instance.id} status {status}"
    )


@receiver(post_save, sender=User)
def set_admin_user_type(sender, instance, created, **kwargs):
    """
    Automatically set user_type to 'admin' for superusers.
    """
    if instance.is_superuser and instance.user_type != "admin":
        User.objects.filter(pk=instance.pk).update(user_type="admin")
