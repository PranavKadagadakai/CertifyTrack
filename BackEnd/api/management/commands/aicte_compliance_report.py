from django.core.management.base import BaseCommand
from django.db.models import Sum, Count, Q
from api.models import Student, AICTEPointTransaction, AICTECategory, Event
import csv
import datetime


class Command(BaseCommand):
    help = 'Generate comprehensive AICTE compliance report'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Output CSV file path (default: aicte_compliance_report.csv)',
            default='aicte_compliance_report.csv'
        )
        parser.add_argument(
            '--department',
            type=str,
            help='Filter by department'
        )
        parser.add_argument(
            '--semester',
            type=int,
            help='Filter by semester'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        department_filter = options.get('department')
        semester_filter = options.get('semester')

        # Query students based on filters
        students_query = Student.objects.all()

        if department_filter:
            students_query = students_query.filter(department=department_filter)
        if semester_filter:
            students_query = students_query.filter(semester=semester_filter)

        students = students_query.order_by('usn')

        # Prepare report data
        report_data = []
        total_students = students.count()
        regular_students = students.filter(admission_type='regular').count()
        lateral_students = students.filter(admission_type='lateral').count()

        self.stdout.write(f'Generating AICTE compliance report for {total_students} students...')

        # Calculate summary statistics
        compliance_stats = {
            'regular_completed': 0,
            'regular_pending': 0,
            'lateral_completed': 0,
            'lateral_pending': 0
        }

        for student in students:
            total_points = student.total_aicte_points
            required_points = student.required_aicte_points
            is_completed = student.is_aicte_completed

            # Count approved and pending transactions
            approved_tx = AICTEPointTransaction.objects.filter(
                student=student, status='APPROVED'
            ).aggregate(total_points=Sum('points_allocated'))['total_points'] or 0

            pending_tx = AICTEPointTransaction.objects.filter(
                student=student, status='PENDING'
            ).count()

            rejected_tx = AICTEPointTransaction.objects.filter(
                student=student, status='REJECTED'
            ).count()

            # Get category breakdown
            category_breakdown = {}
            for tx in AICTEPointTransaction.objects.filter(
                student=student, status='APPROVED'
            ).select_related('category'):
                category_name = tx.category.name
                if category_name not in category_breakdown:
                    category_breakdown[category_name] = 0
                category_breakdown[category_name] += tx.points_allocated

            # Update compliance stats
            if student.admission_type == 'regular':
                if is_completed:
                    compliance_stats['regular_completed'] += 1
                else:
                    compliance_stats['regular_pending'] += 1
            else:  # lateral
                if is_completed:
                    compliance_stats['lateral_completed'] += 1
                else:
                    compliance_stats['lateral_pending'] += 1

            report_data.append({
                'usn': student.usn,
                'name': student.user.get_full_name() or student.user.username,
                'department': student.department,
                'semester': student.semester,
                'admission_type': student.get_admission_type_display(),
                'current_points': total_points,
                'required_points': required_points,
                'points_needed': max(0, required_points - total_points),
                'is_completed': 'Yes' if is_completed else 'No',
                'approved_transactions': approved_tx,
                'pending_transactions': pending_tx,
                'rejected_transactions': rejected_tx,
                'categories_participated': len(category_breakdown),
                'top_categories': ', '.join([
                    f'{cat}: {pts} pts'
                    for cat, pts in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True)[:3]
                ])
            })

        # Write CSV report
        fieldnames = [
            'usn', 'name', 'department', 'semester', 'admission_type',
            'current_points', 'required_points', 'points_needed', 'is_completed',
            'approved_transactions', 'pending_transactions', 'rejected_transactions',
            'categories_participated', 'top_categories'
        ]

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in report_data:
                writer.writerow(row)

        # Print summary
        self.stdout.write(self.style.SUCCESS(f'AICTE Compliance Report Summary:'))
        self.stdout.write(f'Total Students: {total_students}')
        self.stdout.write(f'Regular Students: {regular_students} (Req: 100 points)')
        self.stdout.write(f'  - Completed: {compliance_stats["regular_completed"]}')
        self.stdout.write(f'  - Pending: {compliance_stats["regular_pending"]}')
        self.stdout.write(f'Lateral Entry Students: {lateral_students} (Req: 75 points)')
        self.stdout.write(f'  - Completed: {compliance_stats["lateral_completed"]}')
        self.stdout.write(f'  - Pending: {compliance_stats["lateral_pending"]}')

        overall_completion = (
            (compliance_stats["regular_completed"] + compliance_stats["lateral_completed"])
            / total_students * 100
        ) if total_students > 0 else 0

        self.stdout.write(f'Overall Completion Rate: {overall_completion:.1f}%')
        self.stdout.write(self.style.SUCCESS(f'Report saved to: {output_file}'))
