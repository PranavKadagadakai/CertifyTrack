"""
Management command to set or update email for admin users.
Useful for updating superuser accounts created with createsuperuser without an email.

Usage:
    python manage.py set_admin_email <username> <email>
    python manage.py set_admin_email admin1 admin1@example.com
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from api.models import User


class Command(BaseCommand):
    help = 'Set or update email for an admin user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the admin user')
        parser.add_argument('email', type=str, help='New email address')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            raise CommandError(f'Invalid email format: {email}')

        # Find the user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User with username "{username}" not found')

        # Check if user is admin or superuser
        if user.user_type != 'admin' and not user.is_superuser:
            raise CommandError(f'User "{username}" is not an admin. Cannot set email.')

        # Check if email is already in use
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            raise CommandError(f'Email "{email}" is already in use by another user')

        # Update email and mark as verified
        old_email = user.email
        user.email = email
        user.is_email_verified = True
        user.email_verification_token = None
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Successfully updated email for user "{username}"\n'
                f'  Old email: {old_email or "(none)"}\n'
                f'  New email: {email}\n'
                f'  Email verified: Yes'
            )
        )
