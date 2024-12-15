from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('club', 'Club'), ('mentor', 'Mentor')])

    def __str__(self):
        return self.user.username
