"""
Management command to verify all admin users' emails.
Useful for quickly setting up admin accounts created with createsuperuser.

Usage:
    python manage.py verify_all_admins
"""

from django.core.management.base import BaseCommand
from api.models import User


class Command(BaseCommand):
    help = 'Verify emails for all admin users'

    def handle(self, *args, **options):
        # Get all admin users
        admins = User.objects.filter(user_type='admin')
        superusers = User.objects.filter(is_superuser=True)
        
        # Combine and get unique users
        admin_ids = set(admins.values_list('id', flat=True)) | set(superusers.values_list('id', flat=True))
        admin_users = User.objects.filter(id__in=admin_ids)

        if not admin_users.exists():
            self.stdout.write(self.style.WARNING('No admin users found'))
            return

        # Mark all as verified
        updated_count = admin_users.update(is_email_verified=True, email_verification_token=None)

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Successfully verified emails for {updated_count} admin user(s)\n'
            )
        )

        # List all admins
        self.stdout.write(self.style.SUCCESS('Admin users:'))
        for user in admin_users:
            status = '✓ Verified' if user.is_email_verified else '✗ Not verified'
            email = user.email or '(no email)'
            self.stdout.write(
                f'  • {user.username:<20} | {email:<30} | {status}'
            )
