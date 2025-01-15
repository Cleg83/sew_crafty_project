from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    This signal will update the user's profile when their name or email is updated.
    If a user is created, it will also create a new profile.
    """
    if created:
        # Create user_profile if new user
        UserProfile.objects.create(user=instance)
    else:
        # Update profile if user already exists
        user_profile = instance.userprofile
        user_profile.default_first_name = instance.first_name
        user_profile.default_last_name = instance.last_name
        user_profile.default_email = instance.email
        user_profile.save()