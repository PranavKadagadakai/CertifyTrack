from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile object whenever a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def redirect_to_club_creation(sender, instance, created, **kwargs):
    """
    Redirect users with the 'club' role to the club registration page after profile creation.
    """
    if created and instance.role == 'club':
        # This function cannot directly redirect since it's a signal.
        # Add redirection logic in the frontend or call it in the view
        print(f"Redirect user {instance.user.username} to club registration page.")