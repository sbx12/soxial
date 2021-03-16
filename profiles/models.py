from django.db import models
from django.utils.translation import gettext
from django.urls import reverse

# Models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile/images", blank=True, null=True)
    website_url = models.URLField("Website", blank=True, null=True)
    bio = models.TextField("Bio", blank=True, null=True, default="")
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)
    
    class Meta:
        verbose_name = ("Profile")
        verbose_name_plural = ("Profiles")
        
    def __str__(self):
        return gettext("%(user)s: %(first_name)s %(last_name)s") % {
            "user": self.user,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
    
    def get_absolute_url(self):
        return reverse('public-profile', kwargs={'pk': self.user.pk})