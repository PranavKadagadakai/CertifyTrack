"""
Management command to update user_type to 'admin' for existing superusers.
Useful for migrating superusers created before the signal was implemented.

Usage:
    python manage.py update_superuser_user_types
"""

from django.core.management.base import BaseCommand
from api.models import User


class Command(BaseCommand):
    help = 'Update user_type to admin for existing superusers'

    def handle(self, *args, **options):
        # Find superusers who are not already admin
        superusers_to_update = User.objects.filter(is_superuser=True).exclude(user_type='admin')

        updated_count = 0
        for user in superusers_to_update:
            old_type = user.user_type
            user.user_type = 'admin'
            user.save()
            updated_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Updated {user.username}: {old_type} -> admin'
                )
            )

        if updated_count == 0:
            self.stdout.write(
                self.style.SUCCESS('✓ No superusers needed updating - they are already set to admin')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Updated {updated_count} superuser(s) to admin user_type'
                )
            )
