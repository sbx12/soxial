from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# Models
from django.contrib.auth.models import User

# Serializer
from profiles.api.serializers import (
    UserSerializer
)


class UserProfileDetail(APIView):
    """GET and PUT and delet for Single User Objects"""
    def get(self, request, pk, format=None):
        print("API: Get Selected User")
        user =  get_object_or_404(User.objects.all(), id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)