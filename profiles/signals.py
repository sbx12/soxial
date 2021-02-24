from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.account.models import EmailAddress

# Models
from django.contrib.auth import get_user_model
from profiles.models import Profile
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )
        if not (Token.objects.filter(user=instance).exists()):
            Token.objects.create(user=instance)
        print("Signal: New Profile Created")