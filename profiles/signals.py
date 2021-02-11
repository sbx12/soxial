from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def create_profile(request, user, **kwargs):
    Profile.objects.create(
        user=user
    )
    print("Signal: New Profile Created")