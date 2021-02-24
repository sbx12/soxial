# DRF
from rest_framework import serializers

# Models
from django.contrib.auth.models import User
from posts.models import Post, Comment, Tag

# Serializer
from profiles.api.serializers import UserSerializer, UserMinSerializer


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['name']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    powerup = UserMinSerializer(many=True)
    class Meta:
        model = Comment
        exclude = ['post']
        
        
class CommentFormSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['user', 'post', 'comment']
        

class PostSerializer(serializers.ModelSerializer):    
    user = UserSerializer()
    comment_set = CommentSerializer(many=True)
    powerup = UserMinSerializer(many=True)
    tag = TagSerializer(many=True)
    people_tag = UserMinSerializer(many=True)
    class Meta:
        model= Post
        fields = '__all__'


class PostFormSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Post
        fields = ['user', 'description', 'image', 'tag', 'people_tag']
