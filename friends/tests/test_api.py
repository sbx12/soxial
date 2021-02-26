import json
import tempfile

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from django.contrib.auth import get_user_model
from friends.models import Friend, FriendRequest

DESCRIPTION = "lorem ep sum"
MESSAGE = "lorem ep sum"

class PostAPITest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        print("Friends API Test Begin")
        # Create User1
        cls.user1 = get_user_model().objects.create_user(
            username='testuser100',
            email='testuser100@email.com',
            password='testpass123'
        )
        
        # Create User2
        cls.user2 = get_user_model().objects.create_user(
            username='testuser200',
            email='testuser200@email.com',
            password='testpass123'
        )
        
        # Create User3
        cls.user3 = get_user_model().objects.create_user(
            username='testuser300',
            email='testuser300@email.com',
            password='testpass123'
        )
                        
    def setUp(self):
        # Auth
        self.api_authentication()
        
    def api_authentication(self):
        # Setup Auth
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1.auth_token.key)
        
    def test_create_friend_request(self):
        url = reverse("create-friend-request")
        data = {
            "from_user": self.user1.pk,
            "to_user": self.user2.pk,
            "message": MESSAGE
        }
        response = self.client.post(url, data)
        
        # Check Created Friend Request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['from_user'], self.user1.pk)
        self.assertEqual(response.json()['to_user'], self.user2.pk)
        self.assertEqual(response.json()['message'], MESSAGE)
        
        # Check if users have the Created Friend Request
        self.assertTrue(Friend.objects.get_requests(self.user2.pk).count())
        self.assertTrue(Friend.objects.get_sent_requests(self.user1.pk).count())
        