import uuid
import os
import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.core.exceptions import ValidationError


# ============================================
# VALIDATION FUNCTIONS
# ============================================

# Department to branch code mapping
DEPARTMENT_BRANCH_MAPPING = {
    'CSE': 'CS',
    'AIML': 'AI',
    'ISE': 'IS',
    'Information Science Engineering': 'IS',
    'IS': 'IS',
    'ECE': 'EC',
    'Electrical and Electronics Engineering': 'EC',
    'EEE': 'EE',
    'Electrical and Electronics Engineering': 'EE',
    'ME': 'ME',
    'Mechanical Engineering': 'ME',
    'Civil': 'CV',
    'Civil Engineering': 'CV',
    'Aero': 'AE',
    'Aerospace Engineering': 'AE',
    'Arch': 'AR',
    'Architecture': 'AR'
}

# Reverse mapping for validation
BRANCH_DEPARTMENT_MAPPING = {v: k for k, v in DEPARTMENT_BRANCH_MAPPING.items()}


def validate_usn_format(usn, department):
    """
    Validate USN format: 2GI22{BRANCH}{NUMBER} where NUMBER >= 400 indicates lateral entry
    Regular admission: 001-399, Lateral entry: 400+
    Returns (is_valid, error_message, admission_type)
    """
    if not usn:
        return False, "USN is required", None

    # Pattern: 2GI22XXYYY format where XX is branch code, YYY is student number
    # Examples: 2GI22IS035, 2GI22IS054, 2GI22IS038
    pattern = r'^2GI22([A-Z]{2})(\d{3})$'
    match = re.match(pattern, usn.strip().upper())

    if not match:
        return False, "Invalid USN format. Expected format: 2GI22XX001 where XX is branch code and last 3 digits are 001+", None

    branch_code = match.group(1)
    number_part = match.group(2)
    number_int = int(number_part)

    # Check if branch code matches department
    expected_branch = DEPARTMENT_BRANCH_MAPPING.get(department)
    if not expected_branch:
        return False, f"Unknown department: {department}", None

    if branch_code != expected_branch:
        return False, f"USN branch code '{branch_code}' does not match selected department '{department}' (expected: {expected_branch})", None

    # Determine admission type based on number range
    # Regular admission: 001-399, Lateral entry: 400+
    admission_type = 'lateral' if number_int >= 400 else 'regular'
    return True, None, admission_type


def validate_employee_id_format(employee_id, department):
    """
    Validate Employee ID format: {BRANCH}{NUMBER} where BRANCH is 2 chars, NUMBER is 3 digits
    Returns (is_valid, error_message)
    """
    if not employee_id:
        return False, "Employee ID is required"

    # Pattern: 2 chars for branch + 3 digits for number
    pattern = r'^([A-Z]{2})(\d{3})$'
    match = re.match(pattern, employee_id.strip().upper())

    if not match:
        return False, "Invalid Employee ID format. Expected format: XXYYY where XX is branch code and YYY is number"

    branch_code = match.group(1)

    # Check if branch code matches department
    expected_branch = DEPARTMENT_BRANCH_MAPPING.get(department)
    if not expected_branch:
        return False, f"Unknown department: {department}"

    if branch_code != expected_branch:
        return False, f"Employee ID branch code '{branch_code}' does not match selected department '{department}' (expected: {expected_branch})"

    return True, None


def validate_email_domain(email, user_type):
    """
    Validate email domain based on user type
    Students: @students.git.edu
    Others: @git.edu
    Returns (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    email = email.lower().strip()

    if user_type == 'student':
        if not email.endswith('@students.git.edu'):
            return False, "Students must use @students.git.edu email domain"
    else:
        if not email.endswith('@git.edu'):
            return False, "Faculty/Staff must use @git.edu email domain"

    return True, None


def get_branch_from_usn(usn):
    """
    Extract branch code from USN
    Returns branch code or None if invalid format
    """
    if not usn:
        return None

    pattern = r'^2GI22([A-Z]{2})(\d{3})$'
    match = re.match(pattern, usn.strip().upper())

    if match:
        return match.group(1)
    return None


def get_department_from_branch(branch_code):
    """
    Get department name from branch code
    """
    return BRANCH_DEPARTMENT_MAPPING.get(branch_code)


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
        ('principal', 'Principal'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    verification_sent_at = models.DateTimeField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(blank=True, null=True)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True, help_text="Digital signature for certificate signing (JPEG/PNG)")

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class Student(models.Model):
    ADMISSION_TYPE_CHOICES = (
        ('regular', 'Regular Student'),
        ('lateral', 'Lateral Entry Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    usn = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    admission_type = models.CharField(max_length=10, choices=ADMISSION_TYPE_CHOICES, default='regular')
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

    @property
    def required_aicte_points(self):
        """Return point requirement based on admission type"""
        return 100 if self.admission_type == 'regular' else 75

    @property
    def is_aicte_completed(self):
        """Check if student has met AICTE point requirements"""
        return self.total_aicte_points >= self.required_aicte_points


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
    signature = models.ImageField(upload_to='signatures/mentors/', blank=True, null=True, help_text="Digital signature for certificate signing (JPEG/PNG)")
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
    awardsAictePoints = models.BooleanField(default=False, help_text="Whether event awards AICTE points")
    aicte_category = models.ForeignKey('AICTECategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    points_awarded = models.IntegerField(default=0, help_text="Points awarded per attendance")
    
    # Hall Assignment Fields
    needsVenueCampus = models.BooleanField(default=False, help_text="Whether event requires college campus venue")
    primary_hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='primary_events', help_text="Preferred hall for the event")
    secondary_hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='secondary_events', help_text="Backup hall for the event")
    assigned_hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_events', help_text="Currently assigned hall")
    hall_assigned_at = models.DateTimeField(null=True, blank=True, help_text="When hall was last assigned")

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

    def assign_hall(self):
        """
        Assign a hall to this event based on availability and preferences.
        Returns True if a hall was assigned, False if no hall available.
        """
        from django.utils.timezone import now

        # Check if primary hall is available
        if self.primary_hall and self._is_hall_available(self.primary_hall):
            self.assigned_hall = self.primary_hall
            self.hall_assigned_at = now()
            return True

        # Check if secondary hall is available
        if self.secondary_hall and self._is_hall_available(self.secondary_hall):
            self.assigned_hall = self.secondary_hall
            self.hall_assigned_at = now()
            return True

        # No halls available
        self.assigned_hall = None
        self.hall_assigned_at = now()
        return False

    def _is_hall_available(self, hall):
        """
        Check if a hall is available for this event's date and time.
        """
        return not HallBooking.objects.filter(
            hall=hall,
            booking_date=self.event_date,
            booking_status__in=['APPROVED', 'PENDING'],
            start_time__lt=self.end_time or self.start_time,
            end_time__gt=self.start_time
        ).exists()


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
class PrincipalSignature(models.Model):
    """Global principal signature for certificates across all clubs."""
    signature_image = models.ImageField(
        upload_to='signatures/principal/',
        help_text="Principal's digital signature for certificates (JPEG/PNG)"
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True, help_text="Notes about the signature upload")

    class Meta:
        verbose_name = "Principal Signature"
        verbose_name_plural = "Principal Signatures"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Principal Signature (uploaded {self.uploaded_at.date()})"

    def save(self, *args, **kwargs):
        # Ensure only one active signature at a time
        if self.is_active:
            PrincipalSignature.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


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
    max_points_allowed = models.IntegerField(default=20, help_text="Maximum points that can be awarded (default 20 per VTU rules)")

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
    verification_code = models.CharField(max_length=8, blank=True, null=True, help_text="8-character verification code for mentor approval")
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
    NOTIFICATION_TYPES = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('event_registration', 'Event Registration'),
        ('event_reminder', 'Event Reminder'),
        ('event_cancellation', 'Event Cancellation'),
        ('certificate_generated', 'Certificate Generated'),
        ('points_approved', 'AICTE Points Approved'),
        ('points_rejected', 'AICTE Points Rejected'),
        ('hall_booking_approved', 'Hall Booking Approved'),
        ('hall_booking_rejected', 'Hall Booking Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='info')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)  # Track email delivery
    email_sent_at = models.DateTimeField(blank=True, null=True)

    # Optional related objects for notification context
    event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True)
    aiCTE_transaction = models.ForeignKey('AICTEPointTransaction', on_delete=models.SET_NULL, null=True, blank=True)
    hall_booking = models.ForeignKey('HallBooking', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"


class UserNotificationPreferences(models.Model):
    """User preferences for notification types and delivery methods"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')

    # Email preferences (can be disabled except mandatory ones)
    email_enabled = models.BooleanField(default=True)
    email_event_registrations = models.BooleanField(default=True)
    email_event_reminders = models.BooleanField(default=True)
    email_event_cancellations = models.BooleanField(default=True)
    email_certificate_generation = models.BooleanField(default=True)
    email_aicte_points = models.BooleanField(default=True)
    email_hall_bookings = models.BooleanField(default=True)

    # In-app notification preferences
    in_app_enabled = models.BooleanField(default=True)
    in_app_event_notifications = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification preferences for {self.user.username}"
