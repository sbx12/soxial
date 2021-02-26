from django.db import models

# Utils
from django.utils import timezone

# Models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext

USER_MODEL = get_user_model()

class FriendManager(models.Manager):
    """ Friend Manager """
    def get_friends(self, user):
        return self.filter(to_user=user
            ).select_related("from_user", "to_user")
        
    def get_requests(self, user):
        return FriendRequest.objects.filter(to_user=user
            ).select_related("from_user", "to_user")
    
    def get_sent_requests(self, user):
        return FriendRequest.objects.filter(from_user=user
            ).select_related("from_user", "to_user")

class Friend(models.Model):
    """Used to for Friend Connection"""
    from_user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="_unused_friend_relation")
    to_user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="friends")
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    
    objects = FriendManager()
    
    class Meta:
        verbose_name = "Friend"
        verbose_name_plural = "Friends"

    def __str__(self):
        return gettext("User %(to_user)s homie -> %(from_user)s") % {
            "to_user": self.to_user_id,
            "from_user": self.from_user_id
        }
        

class FriendRequest(models.Model):
    """ Used to represent friend requests made by users """
    from_user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="friendrequest_sent")
    to_user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="friendrequest_received")
    message = models.TextField("Message", blank=True)
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    
    class Meta:
        verbose_name = "Friend Request"
        verbose_name_plural = "Friend Requests"

    def __str__(self):
        return gettext("From User %(from_user)s to -> %(to_user)s") % {
            "from_user": self.from_user_id,
            "to_user": self.to_user_id
        }
        
    def accept(self):
        """ Accept Friend Request """
        # Create an Friend object for both users
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
        
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
        
        # Delete Friend Request since its no longer in use
        self.delete()
        print("accept friend request")
        
    def reject(self):
        """ Reject Friend Request """
        self.delete()
        print("reject friend request")

    def cancel(self):
        """ Cancel Friend Request """
        self.delete()
        print("cancel friend request")
