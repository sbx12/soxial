from django.db import models
from django.utils.translation import gettext

# Models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

USER_MODEL = get_user_model()

class PostManager(models.Manager):
    def get_posts(self, status: bool=False):
        return self.all(
            ).select_related("user__profile"
            ).prefetch_related("power_up__user", "tag__user", "comment_set__user"
            ).order_by("-created_on")


class Post(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField("Description", blank=True, null=True)
    image = models.ImageField(upload_to="post/images", blank=True, null=True)
    power_up = models.ManyToManyField(USER_MODEL, related_name="post_powers", blank=True)
    tag = models.ManyToManyField(USER_MODEL, related_name="tags")
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)
    
    objects = PostManager()
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        
    def __str__(self):
        return gettext("%(user)s: %(description)s[:8]") % {
            "user": self.user.username,
            "description": self.description,
        }
    
    
class Comment(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    power_up = models.ManyToManyField(USER_MODEL, related_name="comment_powers", blank=True)
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ["-created_on"]
        
    def __str__(self):
        return gettext("%(user)s: %(description)s[:8]") % {
            "user": self.user.username,
            "description": self.description,
        }
