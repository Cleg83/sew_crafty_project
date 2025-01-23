from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    This signal will update the user's profile when their name or email is updated.
    If a user is created, it will also create a new profile if it doesn't already exist.
    """
    if created:
        # Only create a new UserProfile if it doesn't already exist
        if not UserProfile.objects.filter(user=instance).exists():
            UserProfile.objects.create(user=instance)
    else:
        # Update profile if user already exists
        user_profile, created = UserProfile.objects.get_or_create(user=instance)
        user_profile.default_first_name = instance.first_name
        user_profile.default_last_name = instance.last_name
        user_profile.default_email = instance.email
        user_profile.save()


@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """
    This signal deletes the user profile when the associated user is deleted.
    Avoid trying to delete a profile if it's already being deleted.
    """
    try:
        user_profile = instance.userprofile
        user_profile.delete()
    except UserProfile.DoesNotExist:
        pass  # No profile to delete