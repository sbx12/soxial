from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser 

# Models
from posts.models import Post, Comment

# Serializer
from posts.api.serializers import (
    PostSerializer, 
    PostFormSerializer,
    CommentFormSerializer
)


# Post Section
class PostList(generics.ListAPIView):
    """List all Posts"""
    queryset = Post.objects.get_posts()
    serializer_class = PostSerializer
    

class PostProfileList(generics.ListAPIView):
    queryset = Post.objects.get_posts()
    
    """List all USER Posts"""
    def list(self, request):
        print("API: Get Profile Post List")
        queryset = get_list_or_404(self.get_queryset().filter(id=self.request.user.pk))
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

class PostCreate(generics.CreateAPIView):
    serializer_class = PostFormSerializer


class PostDetail(APIView):
    """GET and PUT and delet for Single Post  Objects"""
    def get(self, request, pk, format=None):
        print("API: Get Selected Post")
        post =  get_object_or_404(Post.objects.get_posts(), id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        print("API: Update Selected Post")
        post = get_object_or_404(Post.objects.get_posts(), id=pk)
        serializer = PostFormSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, pk, format=None):
        print("API: Delete Selected Post")
        post = get_object_or_404(Post.objects.get_posts(), id=pk)
        post_id = post.id
        post.delete()
        return Response("Post %s has been DELETED" % post_id)


class PostPowerup(APIView):
    def put(self, request, pk, format=None):
        post = get_object_or_404(Post.objects.get_posts(), id=pk)
        if request.data['powerup'] == 'True':
            print("API: Powerup Selected Post")
            post.add_powerup(request.data['user'])
        else:
            print("API: PowerDown Selected Post")
            post.remove_powerup(request.data['user'])
        return Response(status.HTTP_200_OK)


# Comment Section
class CommentDetail(APIView):
    def put(self, request, pk, format=None):
        print("API: Update Selected Comment")
        comment = get_object_or_404(Comment.objects.all(), id=pk)
        serializer = CommentFormSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
    
    def delete(self, request, pk, format=None):
        print("API: Delete Selected Comment")
        comment = get_object_or_404(Comment.objects.all(), id=pk)
        comment.delete()
        return Response(status.HTTP_200_OK)

class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentFormSerializer


class CommentPowerup(APIView):
    def put(self, request, pk, format=None):
        comment = get_object_or_404(Comment.objects.all(), id=pk)
        if request.data['powerup'] == 'True':
            print("API: Powerup Selected Comment")
            comment.add_powerup(request.data['user'])
        else:
            print("API: PowerDown Selected Comment")
            comment.remove_powerup(request.data['user'])
        return Response(status.HTTP_200_OK)