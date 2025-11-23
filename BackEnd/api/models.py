import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.core.exceptions import ValidationError


def certificate_file_path(instance, filename):
    """Build a deterministic, unique path for certificates."""
    ext = os.path.splitext(filename)[1] or '.pdf'
    ext = ext if ext.lower() == '.pdf' else '.pdf'
    event_id = getattr(getattr(instance, 'event', None), 'id', None)
    student_usn = getattr(getattr(instance, 'student', None), 'usn', None)
    if event_id is None:
        event_part = "event_tmp"
    else:
        event_part = f"event_{event_id}"
    if student_usn is None:
        student_part = f"student_{uuid.uuid4().hex[:8]}"
    else:
        student_part = f"usn_{str(student_usn).replace(' ', '_')}"
    filename_safe = f"{event_part}_{student_part}_{uuid.uuid4().hex[:8]}.pdf"
    return os.path.join('certificates', filename_safe)


# ============================================
# USER MANAGEMENT MODELS
# ============================================
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('club_organizer', 'Club Organizer'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    verification_sent_at = models.DateTimeField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    usn = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/students/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    profile_completed = models.BooleanField(default=False)
    profile_completed_at = models.DateTimeField(blank=True, null=True)
    mentor = models.ForeignKey('Mentor', on_delete=models.SET_NULL, null=True, blank=True, related_name='mentees')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.usn})"

    @property
    def total_aicte_points(self):
        return self.aicte_transactions.filter(status='APPROVED').aggregate(total=models.Sum('points_allocated'))['total'] or 0


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/mentors/', blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_completed = models.BooleanField(default=False)
    profile_completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.employee_id})"


class ClubOrganizer(models.Model):
    """Club organizer profile - belongs to one club assigned by admin."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='club_organizer_profile')
    club = models.ForeignKey('Club', on_delete=models.SET_NULL, null=True, blank=True, related_name='organizers')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/club_organizers/', blank=True, null=True)
    designation_in_club = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_completed = models.BooleanField(default=False)
    profile_completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} (Club Organizer)"


# ============================================
# CLUB MANAGEMENT MODELS
# ============================================
class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    faculty_coordinator = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True, related_name='coordinated_clubs')
    club_head = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_clubs')
    established_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ClubRole(models.Model):
    ROLE_CHOICES = (
        ('president', 'President'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer'),
        ('coordinator', 'Coordinator'),
        ('member', 'Member'),
    )
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    can_create_events = models.BooleanField(default=False)
    can_edit_events = models.BooleanField(default=False)
    can_delete_events = models.BooleanField(default=False)
    can_start_events = models.BooleanField(default=False)
    can_end_events = models.BooleanField(default=False)
    can_mark_attendance = models.BooleanField(default=False)
    can_manage_bookings = models.BooleanField(default=False)
    can_upload_templates = models.BooleanField(default=False)
    can_generate_certificates = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    can_manage_members = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='club_memberships')
    role = models.ForeignKey(ClubRole, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('club', 'student')

    def __str__(self):
        return f"{self.student.user.username} - {self.club.name} ({self.role.name})"


# ============================================
# HALL MANAGEMENT MODELS
# ============================================
class Hall(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=200, blank=True)
    capacity = models.IntegerField()
    facilities = models.JSONField(blank=True, null=True)
    is_available = models.BooleanField(default=True)


class HallBooking(models.Model):
    BOOKING_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    )
    
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='hall_bookings')
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hall_bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_bookings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['booking_date', 'hall']),
            models.Index(fields=['booking_status']),
        ]

    def __str__(self):
        return f"Booking {self.id} - {self.hall.name} on {self.booking_date}"


# ============================================
# EVENT MANAGEMENT MODELS
# ============================================
class Event(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True, help_text="For multi-day events. If null, event is single-day")
    max_participants = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # AICTE Points Configuration
    aicte_category = models.ForeignKey('AICTECategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    points_awarded = models.IntegerField(default=0, help_text="Points awarded per attendance")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-event_date', '-start_time']

    def __str__(self):
        return f"{self.name} ({self.event_date})"

    def clean(self):
        if self.end_date and self.end_date < self.event_date:
            raise ValidationError("End date must be after or equal to start date")


class EventAttendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('event', 'student')
        indexes = [models.Index(fields=['event', 'student'])]

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.usn} - {self.event.name} ({status})"


class EventRegistration(models.Model):
    REGISTRATION_STATUS_CHOICES = (
        ('REGISTERED', 'Registered'),
        ('ATTENDED', 'Attended'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    )
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='event_registrations')
    registration_date = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS_CHOICES, default='REGISTERED')

    class Meta:
        unique_together = ('event', 'student')
        indexes = [
            models.Index(fields=['event', 'status']),
            models.Index(fields=['student', 'registration_date']),
        ]

    def __str__(self):
        return f"{self.student.usn} registered for {self.event.name}"


# ============================================
# CERTIFICATE TEMPLATE MANAGEMENT
# ============================================
class CertificateTemplate(models.Model):
    name = models.CharField(max_length=100, default='Global Certificate Template')
    template_file = models.FileField(upload_to='certificate_templates/', help_text="Global certificate template (HTML/PDF)")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    version = models.IntegerField(default=1)
    
    class Meta:
        verbose_name_plural = "Certificate Templates"
    
    def __str__(self):
        return f"{self.name} (v{self.version})"


# ============================================
# CERTIFICATE MANAGEMENT MODELS
# ============================================
class Certificate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='certificates')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to=certificate_file_path, max_length=500, blank=True, null=True, editable=False)
    file_hash = models.CharField(max_length=128, editable=False, null=True, help_text="SHA256 of the certificate file for verification.")
    issue_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"Certificate for {self.student.usn} - Event {getattr(self.event, 'id', 'N/A')}"


# ============================================
# AICTE POINTS MANAGEMENT MODELS
# ============================================
class AICTECategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    min_points_required = models.IntegerField(blank=True, null=True)
    max_points_allowed = models.IntegerField(blank=True, null=True)

    def clean(self):
        if (self.min_points_required is not None) and (self.max_points_allowed is not None):
            if self.min_points_required > self.max_points_allowed:
                raise ValidationError("min_points_required cannot be greater than max_points_allowed")


class AICTEPointTransaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='aicte_transactions')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='aicte_transactions')
    category = models.ForeignKey(AICTECategory, on_delete=models.CASCADE, related_name='transactions')
    points_allocated = models.IntegerField()
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_transactions')
    approval_date = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['event', 'category']),
        ]
        ordering = ['-created_at']

    def clean(self):
        if self.category:
            minp = self.category.min_points_required
            maxp = self.category.max_points_allowed
            if minp is not None and self.points_allocated < minp:
                raise ValidationError(f"points_allocated ({self.points_allocated}) is below category minimum ({minp}).")
            if maxp is not None and self.points_allocated > maxp:
                raise ValidationError(f"points_allocated ({self.points_allocated}) exceeds category maximum ({maxp}).")


# ============================================
# AUDIT LOGGING MODELS
# ============================================
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


# ============================================
# NOTIFICATION MANAGEMENT MODELS
# ============================================
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"