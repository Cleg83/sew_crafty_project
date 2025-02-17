from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_first_name = models.CharField(max_length=30, null=True, blank=True)
    default_last_name = models.CharField(max_length=30, null=True, blank=True)
    default_email = models.EmailField(null=True, blank=True)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_address_1 = models.CharField(max_length=80, null=True, blank=True)
    default_address_2 = models.CharField(max_length=80, null=True, blank=True)
    default_town = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=20, null=True, blank=True)    
    default_postcode = models.CharField(max_length=20, null=True, blank=True)    
    default_country = CountryField(blank_label='Country *', null=True, blank=True)

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()