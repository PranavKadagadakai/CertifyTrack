"""
Django management command to generate verification codes for existing AICTE point transactions
that don't have verification codes yet.
"""
import secrets
import string
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import AICTEPointTransaction


class Command(BaseCommand):
    help = 'Generate verification codes for AICTE point transactions that have null verification_code'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run in dry-run mode (no actual database changes)',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Number of records to process in each batch (default: 1000)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        batch_size = options['batch_size']

        # Query transactions with null verification_code
        transactions_to_update = AICTEPointTransaction.objects.filter(verification_code__isnull=True)

        total_count = transactions_to_update.count()

        if total_count == 0:
            self.stdout.write(
                self.style.SUCCESS('No transactions found with null verification_code. All transactions already have codes.')
            )
            return

        self.stdout.write(
            self.style.WARNING(
                f'Found {total_count} AICTE point transactions with null verification_code.'
            )
        )

        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE: No actual database changes will be made.')
            )

        # Process in batches to avoid memory issues
        updated_count = 0
        batch_num = 1

        while True:
            # Get next batch of transactions
            batch = list(transactions_to_update[:batch_size])
            if not batch:
                break

            batch_count = len(batch)
            self.stdout.write(f'Processing batch {batch_num} ({batch_count} records)...')

            if not dry_run:
                try:
                    with transaction.atomic():
                        for tx in batch:
                            # Generate verification code using same logic as views.py
                            verification_code = ''.join(
                                secrets.choice(string.ascii_letters + string.digits)
                                for _ in range(8)
                            )
                            tx.verification_code = verification_code
                            tx.save(update_fields=['verification_code'])

                        updated_count += batch_count

                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Batch {batch_num}: {batch_count} transactions updated')
                    )

                except Exception as e:
                    raise CommandError(f'Error processing batch {batch_num}: {str(e)}')
            else:
                updated_count += batch_count
                self.stdout.write(f'  ✓ Would update {batch_count} transactions in batch {batch_num}')

            # Remove processed transactions from queryset for next batch
            transactions_to_update = transactions_to_update[batch_size:]
            batch_num += 1

        # Final summary
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'\nDRY RUN COMPLETE: Would update {updated_count} transactions')
            )
        else:
            # Verify the update worked
            remaining_null = AICTEPointTransaction.objects.filter(verification_code__isnull=True).count()
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nUPDATE COMPLETE: {updated_count} transactions updated successfully.'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(f'Transactions with null verification_code remaining: {remaining_null}')
            )

        if not dry_run:
            self.stdout.write(
                self.style.WARNING(
                    '\nNote: You should now regenerate any certificates that were generated before this update '
                    'to include the new verification codes in their QR codes.'
                )
            )
