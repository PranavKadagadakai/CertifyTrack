import uuid
from django.db import models
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError
# from django.utils import timezone

# Club Model
class Club(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Ensure club name is unique
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_club')  # Link one admin to one club
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    club = models.ForeignKey('Cert.Club', on_delete=models.CASCADE, related_name='events')
    status = models.CharField(
        max_length=15,
        choices=[
            ('not_started', 'Not Started'),
            ('started', 'Started'),
            ('finished', 'Finished'),
        ],
        default='not_started'
    )
    template = models.OneToOneField(
        'Cert.CertificateTemplate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='event_template',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    aicte_points = models.IntegerField(default=0)
    participant_limit = models.IntegerField(default=100)
    constraints = models.JSONField(default=dict)  # Example: {"semester": [1, 2], "branch": ["CSE", "ECE"]}

    def __str__(self):
        return f"{self.name} ({self.club.name})"


# Participant Model
class Participant(models.Model):
    event = models.ForeignKey(
        'Cert.Event',
        on_delete=models.CASCADE,
        related_name='participant_records'  # Avoid naming conflict
    )
    student = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='event_participations'
    )

    class Meta:
        unique_together = ('event', 'student')  # Ensure a student can register for an event only once

    def __str__(self):
        return f"{self.student.username} in {self.event.name}"


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    role = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('club', 'Club'),
            ('mentor', 'Mentor'),
            ('admin', 'Admin'),
        ],
        default='student'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    aicte_points = models.IntegerField(default=0)  # AICTE points for students
    usn = models.CharField(max_length=10, unique=True, blank=True, null=True, db_index=True)  # USN is optional for non-students
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentees')
    
    def clean(self):
        # Validate USN format only for students
        if self.role == 'student' and self.usn:
            pattern = r"^\d{2}[A-Z]{2}\d{2}[A-Z]{2}\d{3}$"
            if not re.match(pattern, self.usn):
                raise ValidationError("USN must follow the pattern: 2GI22IS001.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation runs before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# CertificateTemplate Model
class CertificateTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.OneToOneField(
        'Cert.Event',
        on_delete=models.CASCADE,
        related_name='certificate_template',
        null=True,
        blank=True,
    )
    template_file = models.FileField(upload_to='certificate_templates/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Template for {self.event.name if self.event else 'No Event Assigned'}"


# Certificate Model
class Certificate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='certificates')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=None, null=True, related_name='certificate')
    generated_file = models.BinaryField(default=b'')  # Store binary data for the certificate
    generated_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    
    def is_pdf(self):
        # Check the first few bytes of the binary data (PDF files start with "%PDF")
        if self.event.certificate_template.template_file[:4] == b'%PDF':
            return True
        return False
    
    def __str__(self):
        if self.participant:
            return f"Certificate for {self.participant.student.username} - {self.event.name}"
        return f"Certificate for Unknown Participant - {self.event.name}"

    def __str__(self):
        return f"Certificate for {self.participant.student.username} - {self.event.name}"
