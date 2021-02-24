from django.db import models
from django.utils.translation import gettext

# Models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

USER_MODEL = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=40)
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ["-created_on"]
        
    def __str__(self):
        return gettext("%(name)s") % {
            "name": self.name,
        }
    

class PostManager(models.Manager):
    def get_posts(self, status: bool=False):
        return self.all(
            ).select_related("user__profile"
            ).prefetch_related("powerup__profile", "tag", "people_tag__profile", "comment_set__powerup__profile"
            ).order_by("-created_on")
    

class Post(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField("Description", blank=True, null=True)
    image = models.ImageField(upload_to="post/images", blank=True, null=True)
    powerup = models.ManyToManyField(USER_MODEL, related_name="post_powerups", blank=True)
    tag = models.ManyToManyField(Tag, related_name="tags", blank=True)
    people_tag = models.ManyToManyField(USER_MODEL, related_name="people_tags", blank=True)
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)
    
    objects = PostManager()
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        
    def __str__(self):
        return gettext("%(user)s: %(description)s") % {
            "user": self.user.username,
            "description": self.description,
        }
        
    def add_powerup(self, user):
        """Add a Powerup to the Post"""
        self.powerup.add(user)
    
    def remove_powerup(self, user):
        """Remove a Powerup to the Post"""
        self.powerup.remove(user)
        
    
class Comment(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    powerup = models.ManyToManyField(USER_MODEL, related_name="comment_powerups", blank=True)
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)
        
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ["-created_on"]
        
    def __str__(self):
        return gettext("%(user)s: %(comment)s") % {
            "user": self.user.username,
            "comment": self.comment,
        }

    def add_powerup(self, user):
        """Add a Powerup to the Comment"""
        self.powerup.add(user)
    
    def remove_powerup(self, user):
        """Remove a Powerup to the Comment"""
        self.powerup.remove(user)
        
