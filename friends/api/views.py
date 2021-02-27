from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# Models
from django.contrib.auth.models import User
from friends.models import Friend, FriendRequest

# Serializer
from friends.api.serializers import (
    FriendSerializer,
    FriendRequestSerializer,
    FriendRequestFormSerializer
)


class FriendList(generics.ListAPIView):
    """ Get All of Users Friends """
    def list(self, request):
        print("API: Get User Friends")
        queryset = get_list_or_404(Friend.objects.get_friends(self.request.user))
        serializer = FriendSerializer(queryset, many=True)
        return Response(serializer.data)
    

class FriendDetail(APIView):
    """GET and PUT and Delete for Single Friend Object"""
    def delete(self, request, pk, format=None):
        print("API: Delete Selected Friend")
        friend = get_object_or_404(User.objects.all(), id=pk)
        Friend.objects.delete_friends(self.request.user, friend)
        return Response(status=status.HTTP_200_OK)
        

class FriendRequestList(generics.ListAPIView):
    """ Get All of Users Pending Friend Request """
    def list(self, request):
        print("API: Get User Friend Request")
        queryset = get_list_or_404(Friend.objects.get_requests(self.request.user))
        serializer = FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class FriendSentRequestList(generics.ListAPIView):
    """ Get All of Users Sent Friend Request """
    def list(self, request):
        print("API: Get User Sent Friend Request")
        queryset = get_list_or_404(Friend.objects.get_sent_requests(self.request.user))
        serializer = FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)
    

class FriendSentRequestCreate(generics.CreateAPIView):
    serializer_class = FriendRequestFormSerializer
    

class FriendRequestDetail(APIView):
    """GET and PUT and delet for Single Friend Request  Objects"""
    def get(self, request, pk, format=None):
        print("API: Get Selected Friend Request")
        friend_request =  get_object_or_404(FriendRequest.objects.all(), id=pk)
        serializer = FriendRequest(friend_request)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        print("API: Update Selected Friend Request")
        friend_request = get_object_or_404(FriendRequest.objects.all(), id=pk)
        if request.data['accept'] == 'True':
            friend_request.accept()
            return Response(status=status.HTTP_201_CREATED)
        else:
            friend_request.reject()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        print("API: Delete Selected Friend Request")
        friend_request = get_object_or_404(FriendRequest.objects.all(), id=pk)
        friend_request.cancel()
        return Response(status=status.HTTP_200_OK)