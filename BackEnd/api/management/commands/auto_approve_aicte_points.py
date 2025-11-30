from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from api.models import AICTEPointTransaction, AuditLog


class Command(BaseCommand):
    help = 'Auto-approve AICTE point transactions older than 7 days'

    def handle(self, *args, **options):
        # Find transactions older than 7 days that are still pending
        cutoff_date = now() - timedelta(days=7)
        pending_transactions = AICTEPointTransaction.objects.filter(
            status='PENDING',
            created_at__lt=cutoff_date
        )

        approved_count = 0
        for transaction in pending_transactions:
            transaction.status = 'APPROVED'
            transaction.approval_date = now()
            transaction.approved_by = None  # Auto-approved, no specific user
            transaction.save()
            approved_count += 1

            # Log approval
            AuditLog.objects.create(
                user=transaction.student.user,
                action=f"Auto-approved AICTE transaction ID {transaction.id} after 7 days"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully auto-approved {approved_count} AICTE point transactions older than 7 days.'
            )
        )
