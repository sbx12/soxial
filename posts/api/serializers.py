# DRF
from rest_framework import serializers

# Models
from django.contrib.auth.models import User
from posts.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        

class PostSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)
    class Meta:
        model= Post
        fields = '__all__'
