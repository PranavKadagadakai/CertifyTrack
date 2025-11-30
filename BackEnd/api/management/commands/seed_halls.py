"""
Management command to seed sample halls/venues into the database.
"""
from django.core.management.base import BaseCommand
from api.models import Hall


class Command(BaseCommand):
    help = 'Seed the database with sample halls/venues'

    def handle(self, *args, **options):
        halls_data = [
            {
                'name': 'MV Hall',
                'code': 'MV',
                'location': 'Main Building Ground floor',
                'capacity': 150,
                'facilities': ['Projector', 'Sound System', 'Microphone', 'WiFi'],
                'is_available': True,
            },
            {
                'name': 'SJ Auditorium',
                'code': 'SJ-AUD',
                'location': 'Besides MBA Block',
                'capacity': 400,
                'facilities': ['Projector', 'Sound System', 'Microphone', 'WiFi', 'AC'],
                'is_available': True,
            },
            {
                'name': 'Architecture Block',
                'code': 'ARCH',
                'location': 'Architecture Dept. Block',
                'capacity': 100,
                'facilities': ['Projector', 'Sound System', 'Microphone', 'WiFi'],
                'is_available': True,
            },
        ]

        created_count = 0
        for hall_data in halls_data:
            hall, created = Hall.objects.get_or_create(
                code=hall_data['code'],
                defaults=hall_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created hall: {hall.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⊙ Hall already exists: {hall.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully seeded {created_count} new halls!')
        )
