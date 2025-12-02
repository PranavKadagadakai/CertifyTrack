from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from api.models import Event, Notification


class Command(BaseCommand):
    help = 'Automatically update event statuses based on current date and time'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without actually changing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        now = timezone.now()

        # Log the start of the process
        self.stdout.write(f"Starting event status update at {now}")

        # Get all events that could potentially be updated
        events = Event.objects.exclude(status__in=['completed', 'cancelled'])

        if dry_run:
            self.stdout.write("DRY RUN - No changes will be made")

        # Track changes for reporting
        status_changes = {
            'draft_to_scheduled': [],
            'scheduled_to_ongoing': [],
            'ongoing_to_completed': [],
            'scheduled_to_completed': [],
        }

        # 1. Update draft events to scheduled
        # An event becomes scheduled when:
        # - It's currently draft
        # - The event date is today or in the past (for recurring/scheduled events)
        # - OR the event is meant to start soon (within a reasonable time window)

        for event in events.filter(status='draft'):
            should_be_scheduled = (
                event.event_date <= now.date() or
                (event.event_date == now.date() and event.start_time <= now.time())
            )

            if should_be_scheduled:
                status_changes['draft_to_scheduled'].append(event)
                if not dry_run:
                    event.status = 'scheduled'
                    event.save()

                    # Create notification for club organizer
                    if event.club and hasattr(event.club, 'organizers') and event.club.organizers.exists():
                        club_organizer = event.club.organizers.first()
                        organizer = club_organizer.user
                        Notification.objects.create(
                            user=organizer.user,
                            title="Event Status Updated",
                            message=f"Your event '{event.name}' has been automatically set to scheduled status.",
                            notification_type="info",
                            event=event
                        )

                    self.stdout.write(f"  Updated {event.name} from draft to scheduled")

        # 2. Update scheduled events
        # A scheduled event becomes ongoing when:
        # - It's on the event date and current time >= start time
        # - OR it's during a multi-day event period

        for event in events.filter(status='scheduled'):
            is_current_date = (
                event.event_date == now.date() or
                (event.end_date and event.event_date <= now.date() <= event.end_date)
            )

            if is_current_date:
                # Check if event should start (becoming ongoing)
                time_based_condition = event.start_time <= now.time()

                if time_based_condition:
                    # Determine if it's a single-day event becoming ongoing,
                    # or should go directly to completed
                    should_be_completed = (
                        event.end_time and
                        now.time() >= event.end_time and
                        not event.end_date  # Single day event
                    )

                    if should_be_completed:
                        status_changes['scheduled_to_completed'].append(event)
                        if not dry_run:
                            event.status = 'completed'
                            event.save()

                            # Create notification
                            self._create_status_notification(event, 'completed')
                            self.stdout.write(f"  Updated {event.name} from scheduled to completed")
                    else:
                        status_changes['scheduled_to_ongoing'].append(event)
                        if not dry_run:
                            event.status = 'ongoing'
                            event.save()

                            # Create notification
                            self._create_status_notification(event, 'ongoing')
                            self.stdout.write(f"  Updated {event.name} from scheduled to ongoing")

        # 3. Update ongoing events to completed
        # An ongoing event becomes completed when:
        # - Current time >= end time on the event date
        # - OR for multi-day events, when we've passed the end date

        for event in events.filter(status='ongoing'):
            should_be_completed = False

            if event.end_date:
                # Multi-day event
                if now.date() > event.end_date:
                    should_be_completed = True
                elif now.date() == event.end_date and event.end_time and now.time() >= event.end_time:
                    should_be_completed = True
            else:
                # Single-day event
                if now.date() == event.event_date and event.end_time and now.time() >= event.end_time:
                    should_be_completed = True

            if should_be_completed:
                status_changes['ongoing_to_completed'].append(event)
                if not dry_run:
                    event.status = 'completed'
                    event.save()

                    # Create notification
                    self._create_status_notification(event, 'completed')
                    self.stdout.write(f"  Updated {event.name} from ongoing to completed")

        # Report results
        total_changes = sum(len(events) for events in status_changes.values())

        self.stdout.write(f"\nSummary of status changes:")
        self.stdout.write(f"  Draft → Scheduled: {len(status_changes['draft_to_scheduled'])} events")
        self.stdout.write(f"  Scheduled → Ongoing: {len(status_changes['scheduled_to_ongoing'])} events")
        self.stdout.write(f"  Scheduled → Completed: {len(status_changes['scheduled_to_completed'])} events")
        self.stdout.write(f"  Ongoing → Completed: {len(status_changes['ongoing_to_completed'])} events")
        self.stdout.write(f"  Total: {total_changes} events updated")

        if dry_run:
            self.stdout.write("DRY RUN COMPLETE - No database changes were made")
        else:
            self.stdout.write("Event status update completed successfully")

    def _create_status_notification(self, event, new_status):
        """Create notification for status change"""
        status_messages = {
            'ongoing': f"Your event '{event.name}' is now ongoing.",
            'completed': f"Your event '{event.name}' has been completed."
        }

        message = status_messages.get(new_status, f"Your event '{event.name}' status has been updated to {new_status}.")

        if event.club and hasattr(event.club, 'organizers') and event.club.organizers.exists():
            club_organizer = event.club.organizers.first()
            Notification.objects.create(
                user=club_organizer.user,
                title="Event Status Updated",
                message=message,
                notification_type="info",
                event=event
            )
