"""
Management command to clean up duplicate records across multiple tables.
Specifically handles AICTE transactions and other tables that might have duplicates.
"""

from django.core.management.base import BaseCommand
from django.db.models import Count
from api.models import AICTEPointTransaction, Certificate, EventAttendance, EventRegistration


class Command(BaseCommand):
    help = 'Clean up duplicate records across multiple tables'

    def handle(self, *args, **options):
        cleaned_total = 0

        # 1. Clean AICTE Transactions
        cleaned_aicte = self.clean_aicte_transactions()
        cleaned_total += cleaned_aicte

        # 2. Clean Certificate duplicates
        cleaned_certs = self.clean_certificate_duplicates()
        cleaned_total += cleaned_certs

        # 3. Check EventAttendance (should already be unique but verify)
        self.check_event_attendance()

        # 4. Check EventRegistration (should already be unique but verify)
        self.check_event_registration()

        if cleaned_total > 0:
            self.stdout.write(self.style.SUCCESS(f'Total cleaned records: {cleaned_total}'))
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate records found.'))

    def clean_aicte_transactions(self):
        """Clean duplicate AICTE transactions for same student-event pairs"""
        self.stdout.write('\n=== Cleaning AICTE Transactions ===')

        # Find duplicates
        duplicates = AICTEPointTransaction.objects.values('student', 'event') \
            .annotate(count=Count('pk')).filter(count__gt=1)

        if not duplicates:
            self.stdout.write('No duplicate AICTE transactions found.')
            return 0

        self.stdout.write(f'Found {len(duplicates)} groups of duplicate transactions...')

        cleaned = 0
        total_groups = len(duplicates)

        for i, dup in enumerate(duplicates, 1):
            student_id = dup['student']
            event_id = dup['event']

            # Get all transactions for this pair
            transactions = AICTEPointTransaction.objects.filter(
                student=student_id, event=event_id
            ).order_by('-updated_at')

            self.stdout.write(f'Processing group {i}/{total_groups}: Student {student_id}, Event {event_id}')

            # Show current points before cleanup
            total_before = sum(t.points_allocated for t in transactions.filter(status='APPROVED'))
            self.stdout.write(f'  Total approved points before: {total_before}')

            # Priority: Always combine APPROVED transactions into one
            approved_transactions = transactions.filter(status='APPROVED')

            if approved_transactions.exists():
                # Combine ALL approved transactions into ONE record
                combined_transaction = approved_transactions.first()
                total_approved_points = sum(t.points_allocated for t in approved_transactions)
                combined_transaction.points_allocated = total_approved_points
                combined_transaction.save()
                self.stdout.write(f'  Combined {approved_transactions.count()} approved transactions, final points: {total_approved_points}')

                # Delete all other approved transactions for this student-event
                approved_to_delete = approved_transactions.exclude(pk=combined_transaction.pk)
                if approved_to_delete.exists():
                    deleted_count = approved_to_delete.delete()[0]
                    cleaned += deleted_count
                    self.stdout.write(f'  Deleted {deleted_count} duplicate approved transactions')

                # Delete ALL pending transactions for this student-event (keep only approved)
                pending_transactions = transactions.filter(status='PENDING')
                if pending_transactions.exists():
                    deleted_count = pending_transactions.delete()[0]
                    cleaned += deleted_count
                    self.stdout.write(f'  Deleted {deleted_count} pending transactions (keeping only approved)')

            else:
                # No approved transactions: keep only the most recent PENDING
                most_recent = transactions.filter(status='PENDING').first()
                if most_recent:
                    pending_to_delete = transactions.filter(status='PENDING').exclude(pk=most_recent.pk)
                    if pending_to_delete.exists():
                        deleted_count = pending_to_delete.delete()[0]
                        cleaned += deleted_count
                        self.stdout.write(f'  Kept most recent pending, deleted {deleted_count} older pending')
                else:
                    # No approved or pending? This shouldn't happen, but clean all
                    deleted_count = transactions.delete()[0]
                    cleaned += deleted_count
                    self.stdout.write(f'  Deleted {deleted_count} invalid transactions')

        # Final verification: Check total points for each student that had duplicates
        self.stdout.write('\n=== Verifying Cleanup Results ===')
        affected_students = set()

        for dup in duplicates:
            student = dup['student']
            affected_students.add(student)

        for student_id in affected_students[:10]:  # Check first 10 to avoid too much output
            from api.models import Student
            try:
                student = Student.objects.get(id=student_id)
                total_points = student.total_aicte_points
                self.stdout.write(f'Student {student_id} ({student.user.username}): {total_points} points')
            except:
                pass

        if len(affected_students) > 10:
            self.stdout.write(f'... and {len(affected_students) - 10} more students checked')

        self.stdout.write(self.style.SUCCESS(f'Cleaned up {cleaned} AICTE duplicate transactions.'))
        return cleaned

    def clean_certificate_duplicates(self):
        """Clean duplicate certificates for same event-student pairs"""
        self.stdout.write('\n=== Cleaning Certificate Duplicates ===')

        # Find certificate duplicates
        duplicates = Certificate.objects.values('event', 'student') \
            .annotate(count=Count('pk')).filter(count__gt=1)

        if not duplicates:
            self.stdout.write('No duplicate certificates found.')
            return 0

        self.stdout.write(f'Found {len(duplicates)} groups of duplicate certificates...')

        cleaned = 0
        total_groups = len(duplicates)

        for i, dup in enumerate(duplicates, 1):
            event_id = dup['event']
            student_id = dup['student']

            certificates = Certificate.objects.filter(
                event=event_id, student=student_id
            ).order_by('-issue_date')

            # Keep the most recent certificate, delete others
            most_recent = certificates.first()
            to_delete = certificates.exclude(pk=most_recent.pk)

            if to_delete.exists():
                deleted_count = to_delete.delete()[0]
                cleaned += deleted_count
                self.stdout.write(f'Kept certificate {most_recent.id}, deleted {deleted_count} older duplicates for Event {event_id}, Student {student_id}')

        self.stdout.write(self.style.SUCCESS(f'Cleaned up {cleaned} duplicate certificates.'))
        return cleaned

    def check_event_attendance(self):
        """Check EventAttendance for duplicates (should have unique constraint)"""
        self.stdout.write('\n=== Checking EventAttendance ===')

        duplicates = EventAttendance.objects.values('event', 'student') \
            .annotate(count=Count('pk')).filter(count__gt=1)

        if duplicates:
            self.stdout.write(self.style.ERROR(f'Found {len(duplicates)} EventAttendance duplicates!'))
            for dup in duplicates:
                count = EventAttendance.objects.filter(
                    event=dup['event'], student=dup['student']
                ).count()
                self.stdout.write(f'  Event {dup["event"]}, Student {dup["student"]}: {count} records')
        else:
            self.stdout.write('EventAttendance: No duplicates found.')

    def check_event_registration(self):
        """Check EventRegistration for duplicates (should have unique constraint)"""
        self.stdout.write('\n=== Checking EventRegistration ===')

        duplicates = EventRegistration.objects.values('event', 'student') \
            .annotate(count=Count('pk')).filter(count__gt=1)

        if duplicates:
            self.stdout.write(self.style.ERROR(f'Found {len(duplicates)} EventRegistration duplicates!'))
            for dup in duplicates:
                count = EventRegistration.objects.filter(
                    event=dup['event'], student=dup['student']
                ).count()
                self.stdout.write(f'  Event {dup["event"]}, Student {dup["student"]}: {count} records')
        else:
            self.stdout.write('EventRegistration: No duplicates found.')
