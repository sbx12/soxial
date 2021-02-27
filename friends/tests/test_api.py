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
        
        # Create User3
        cls.user4 = get_user_model().objects.create_user(
            username='testuser400',
            email='testuser400@email.com',
            password='testpass123'
        )
                        
    def setUp(self):       
        self.friend_request = FriendRequest.objects.create(
            from_user=self.user3,
            to_user=self.user4,
            message=MESSAGE
        ) 
        # Auth
        self.api_authentication()
        
    def api_authentication(self):
        # Setup Auth
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1.auth_token.key)
    
    
    # Test Friend
    def test_get_friend_list(self):
        # Create Friend Request
        self.friend1 = Friend.objects.create(
            from_user=self.user1,
            to_user=self.user2,
        )
        
        self.friend2 = Friend.objects.create(
            from_user=self.user1,
            to_user=self.user3,
        )
        
        url = reverse("list-friend")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        
    def test_delete_friend(self):
        # Create Friend Request
        self.friend1 = Friend.objects.create(
            from_user=self.user1,
            to_user=self.user2,
        )
        self.friend2 = Friend.objects.create(
            from_user=self.user2,
            to_user=self.user1,
        )
        self.friend3 = Friend.objects.create(
            from_user=self.user2,
            to_user=self.user3,
        )
        
        url = reverse("detail-friend", args=[self.user2.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Friend.objects.get_friends(self.user1).exists())
        self.assertTrue(Friend.objects.get_friends(self.user2).exists())
    
    # Test Friend Request
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
        self.assertTrue(Friend.objects.get_requests(self.user2.pk).exists())
        self.assertTrue(Friend.objects.get_sent_requests(self.user1.pk).exists())
        
    def test_friend_request_accept(self):
        url = reverse("detail-friend-request", args=[self.friend_request.pk])
        data = {
            "accept": True,
        }
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Friend.objects.get_friends(self.user3).exists())
        self.assertTrue(Friend.objects.get_friends(self.user4).exists())
        
    def test_friend_request_reject(self):
        url = reverse("detail-friend-request", args=[self.friend_request.pk])
        data = {
            "accept": False,
        }
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(FriendRequest.objects.filter(id=self.friend_request.id).exists())
        self.assertFalse(Friend.objects.get_friends(self.user3).exists())
        self.assertFalse(Friend.objects.get_friends(self.user4).exists())
        
    def test_friend_request_cancel(self):
        url = reverse("detail-friend-request", args=[self.friend_request.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(FriendRequest.objects.filter(id=self.friend_request.id).exists())
        
    def test_friend_request_list(self):
        # Create Friend Request
        self.friend_request = FriendRequest.objects.create(
            from_user=self.user3,
            to_user=self.user1,
            message=MESSAGE
        )
        
        self.friend_request = FriendRequest.objects.create(
            from_user=self.user2,
            to_user=self.user1,
            message=MESSAGE
        )
        
        url = reverse("list-friend-request")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        
    def test_friend_sent_request_list(self):
        # Create Friend Request
        self.friend_request = FriendRequest.objects.create(
            from_user=self.user1,
            to_user=self.user3,
            message=MESSAGE
        )
        
        self.friend_request = FriendRequest.objects.create(
            from_user=self.user1,
            to_user=self.user2,
            message=MESSAGE
        )
        
        url = reverse("list-friend-sent-request")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)