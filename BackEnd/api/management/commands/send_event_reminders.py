"""
Management command to send event reminder emails to registered students 24 hours before events.
Run with: python manage.py send_event_reminders
"""
import threading
from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from django.db.models import Q
from api.models import Event, EventRegistration
from api.email_utils import send_event_reminder_email


class Command(BaseCommand):
    help = 'Send event reminder emails to registered students 24 hours before events'

    def handle(self, *args, **options):
        # Calculate the time window (24 +/- 1 hour to handle cron job timing)
        reminder_time_start = now() + timedelta(hours=23)
        reminder_time_end = now() + timedelta(hours=25)

        # Find events starting in the next 24 hours
        upcoming_events = Event.objects.filter(
            Q(event_date=now().date(), start_time__range=(reminder_time_start.time(), reminder_time_end.time())) |
            Q(event_date=(now() + timedelta(days=1)).date(), start_time__range=(reminder_time_start.time(), reminder_time_end.time()))
        ).filter(status__in=['scheduled', 'upcoming'])

        self.stdout.write(f"Found {upcoming_events.count()} events starting in 24 hours")

        reminder_count = 0
        error_count = 0

        for event in upcoming_events:
            # Get all registered students (not cancelled)
            registrations = EventRegistration.objects.filter(
                event=event,
                status__in=['REGISTERED', 'ATTENDED']
            ).select_related('student__user')

            self.stdout.write(f"Sending reminders for event '{event.name}' to {registrations.count()} students")

            for registration in registrations:
                student = registration.student
                try:
                    # Send reminder email asynchronously
                    threading.Thread(target=send_event_reminder_email, args=(student.user, event)).start()
                    reminder_count += 1
                except Exception as e:
                    self.stderr.write(f"Error sending reminder to {student.user.email}: {str(e)}")
                    error_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully sent {reminder_count} event reminders"
            )
        )
        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"{error_count} reminders failed to send"
                )
            )
