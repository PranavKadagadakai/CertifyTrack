import uuid
from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Ensure club name is unique
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_club')  # Link one admin to one club
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('student', 'Student'), ('club', 'Club'), ('mentor', 'Mentor')], default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class CertificateTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID for the CertificateTemplate
    event = models.OneToOneField(
        'Event',
        on_delete=models.CASCADE,
        related_name='certificate_template',
        null=True,  # Allow null for existing rows
    )
    template_file = models.FileField(upload_to='certificate_templates/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Template for {self.event.name if self.event else 'No Event Assigned'}"

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID for the Event
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='events',
    )
    status = models.CharField(max_length=15, choices=[
        ('not_started', 'Not Started'),
        ('started', 'Started'),
        ('finished', 'Finished'),
    ], default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.club.name})"

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID for the Certificate
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='certificates')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    generated_file = models.FileField(upload_to='certificates/%Y/%m/%d/', null=True, blank=True)  # Temporarily allow null
    generated_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Certificate for {self.student.username} - {self.event.name}"
