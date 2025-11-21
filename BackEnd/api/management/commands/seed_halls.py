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
                'name': 'Auditorium A',
                'code': 'AUD-A',
                'location': 'Main Building, Ground Floor',
                'capacity': 500,
                'facilities': ['Projector', 'Sound System', 'Microphone', 'Parking'],
                'is_available': True,
            },
            {
                'name': 'Seminar Hall 1',
                'code': 'SEM-1',
                'location': 'Main Building, First Floor',
                'capacity': 100,
                'facilities': ['Projector', 'WiFi', 'AC'],
                'is_available': True,
            },
            {
                'name': 'Seminar Hall 2',
                'code': 'SEM-2',
                'location': 'Main Building, Second Floor',
                'capacity': 80,
                'facilities': ['Projector', 'WiFi', 'AC'],
                'is_available': True,
            },
            {
                'name': 'Conference Room A',
                'code': 'CONF-A',
                'location': 'Admin Building, First Floor',
                'capacity': 30,
                'facilities': ['Video Conference', 'WiFi', 'AC'],
                'is_available': True,
            },
            {
                'name': 'Conference Room B',
                'code': 'CONF-B',
                'location': 'Admin Building, First Floor',
                'capacity': 25,
                'facilities': ['Video Conference', 'WiFi', 'AC'],
                'is_available': True,
            },
            {
                'name': 'Training Lab',
                'code': 'LAB-T',
                'location': 'IT Building, Ground Floor',
                'capacity': 50,
                'facilities': ['Computers', 'Projector', 'WiFi', 'AC'],
                'is_available': True,
            },
            {
                'name': 'Sports Complex',
                'code': 'SPORTS',
                'location': 'Sports Ground',
                'capacity': 1000,
                'facilities': ['Outdoor Space', 'Sound System', 'Seating'],
                'is_available': True,
            },
            {
                'name': 'Cafeteria',
                'code': 'CAF-1',
                'location': 'Main Building, Ground Floor',
                'capacity': 200,
                'facilities': ['Catering', 'Tables', 'Chairs'],
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
