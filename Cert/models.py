import uuid
from django.db import models
from django.contrib.auth.models import User
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
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    status = models.CharField(
        max_length=15,
        choices=[
            ('not_started', 'Not Started'),
            ('started', 'Started'),
            ('finished', 'Finished'),
        ],
        default='not_started'
    )
    certificate_template = models.BinaryField(blank=True, null=True, editable=True)  # Allow blank for events without a template
    created_at = models.DateTimeField(auto_now_add=True)
    # participants = models.ManyToManyField(Profile, related_name="registered_events", blank=True)

    def __str__(self):
        return f"{self.name} ({self.club.name})"

# Participant Model
class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participations')

    class Meta:
        unique_together = ('event', 'student')  # Ensure each student can participate in an event only once

    def __str__(self):
        return f"{self.student.username} in {self.event.name}"

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('club', 'Club'),
            ('mentor', 'Mentor'),
        ],
        default='student'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    aicte_points = models.IntegerField(default=0)  # AICTE points for students

    def __str__(self):
        return self.user.username

# CertificateTemplate Model
class CertificateTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID for the CertificateTemplate
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name='template',
        null=True,  # Allow null for existing rows without a template
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

    def __str__(self):
        return f"Certificate for {self.participant.student.username} - {self.event.name}"
