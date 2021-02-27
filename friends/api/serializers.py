# DRF
from rest_framework import serializers

# Models
from friends.models import Friend, FriendRequest

# Serializer
from profiles.api.serializers import UserMinSerializer


class FriendSerializer(serializers.ModelSerializer):
    to_user = UserMinSerializer(many=False)
    
    class Meta:
        model = Friend
        fields = '__all__'
        read_only_fields  = ['created_on']
        
        
class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserMinSerializer(many=False)
    to_user = UserMinSerializer(many=False)
    
    class Meta:
        model = FriendRequest
        fields = '__all__'
        read_only_fields = ['created_on']
        
class FriendRequestFormSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FriendRequest
        fields = '__all__'
        read_only_fields = ['created_on']

