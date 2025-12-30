from django.core.management.base import BaseCommand
from api.models import AICTECategory


class Command(BaseCommand):
    help = 'Populate AICTE categories as per VTU Circular No. VTU/BGM/Aca-OS/Cirs/2022-23/5200'

    def handle(self, *args, **options):
        # VTU Specified AICTE Activity Categories
        aicte_categories = [
            {
                'name': 'Helping local schools improve educational outcomes',
                'description': 'Activities aimed at improving access to and quality of education in nearby schools through tutoring, teaching aids, infrastructure support, and educational campaigns.'
            },
            {
                'name': 'Village transformation & income enhancement',
                'description': 'Programs focused on rural development including skill training, entrepreneurship, agriculture improvement, and sustainable livelihood initiatives.'
            },
            {
                'name': 'Sustainable water management development',
                'description': 'Projects related to water conservation, rainwater harvesting, watershed management, and awareness about water usage and purification.'
            },
            {
                'name': 'Tourism promotion & innovation',
                'description': 'Activities promoting local tourism through cultural preservation, heritage promotion, eco-tourism, and innovative tourism solutions.'
            },
            {
                'name': 'Appropriate technology promotion',
                'description': 'Implementation and promotion of affordable, sustainable technologies for rural and community development including solar energy, biogas, etc.'
            },
            {
                'name': 'Energy consumption reduction',
                'description': 'Awareness campaigns and initiatives focused on reducing energy consumption through conservation, efficiency improvements, and renewable energy adoption.'
            },
            {
                'name': 'Rural skill development',
                'description': 'Training programs and workshops for skill development in rural areas including vocational training, crafts, and traditional knowledge preservation.'
            },
            {
                'name': 'Digital money/financial literacy',
                'description': 'Programs educating communities about digital financial services, banking, insurance, and financial planning for better economic literacy.'
            },
            {
                'name': 'Women\'s empowerment & socio-economic awareness',
                'description': 'Initiatives focused on women\'s education, healthcare, economic participation, and creating awareness about social and economic rights.'
            },
            {
                'name': 'Garbage disposal/solid waste management',
                'description': 'Community programs for waste segregation, recycling, composting, and creating awareness about proper waste disposal practices.'
            },
            {
                'name': 'Rural produce marketing support',
                'description': 'Support for farmer producer organizations, direct marketing, e-commerce platforms for agricultural products, and value addition to rural produce.'
            },
            {
                'name': 'Food preservation & packaging',
                'description': 'Training and implementation of food preservation techniques, modern packaging methods, and value addition to prevent food wastage.'
            },
            {
                'name': 'Local automation initiatives',
                'description': 'Development and deployment of automation solutions for local industries, agriculture, and community services using appropriate technologies.'
            },
            {
                'name': 'Public awareness under rural outreach',
                'description': 'General awareness campaigns on health, sanitation, education, government schemes, and community development issues in rural areas.'
            },
            {
                'name': 'Participation in national-level government initiatives',
                'description': 'Active participation in national programs like Swachh Bharat, Digital India, Skill India, Beti Bachao Beti Padhao, and other government initiatives.'
            },
            {
                'name': 'Rainwater harvesting awareness',
                'description': 'Programs creating awareness about rainwater harvesting techniques, implementation of harvesting systems, and water management practices.'
            }
        ]

        created_count = 0
        for category_data in aicte_categories:
            category, created = AICTECategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'min_points_required': 5,  # Minimum points required to qualify
                    'max_points_allowed': 20  # Per VTU rules, max 20 points per activity
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully seeded {created_count} AICTE categories. '
                f'Total categories in database: {AICTECategory.objects.count()}'
            )
        )
