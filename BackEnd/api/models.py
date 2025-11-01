import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('club', 'Club'),
        ('mentor', 'Mentor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    full_name = models.CharField(max_length=255, blank=True)
    usn = models.CharField(max_length=10, unique=True, null=True, blank=True)
    aicte_points = models.IntegerField(default=0)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentees')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Club(models.Model):
    name = models.CharField(max_length=255, unique=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_club')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CertificateTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template_file = models.FileField(upload_to='certificate_templates/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('started', 'Started'),
        ('finished', 'Finished'),
    )
    name = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    aicte_points = models.IntegerField(default=0)
    participant_limit = models.PositiveIntegerField(default=100)
    template = models.OneToOneField(CertificateTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.club.name}"

class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')

    class Meta:
        unique_together = ('event', 'student')

    def __str__(self):
        return f"{self.student.username} in {self.event.name}"

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='certificates')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='certificates')
    certificate_file = models.FileField(upload_to='generated_certificates/')
    generated_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Certificate for {self.participant.student.username} in {self.event.name}"