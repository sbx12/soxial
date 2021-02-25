import json
import tempfile

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from django.contrib.auth import get_user_model

WEBSITE_URL = "https://www.youtube.com/"
BIO = "Lorem Ep Sum"

class ProfilesAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        print("Posts API Test Begin")
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
        
    def setUp(self):
        # Create User3
        self.user3 = get_user_model().objects.create_user(
            username='testuser300',
            email='testuser300@email.com',
            password='testpass123'
        )
        self.user3.profile.website_url = WEBSITE_URL
        self.user3.profile.bio = BIO
        print(self.user3.profile.bio)
        # Auth
        self.api_authentication()

    def api_authentication(self):
        # Setup Auth
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1.auth_token.key)
        
    def test_get_userprofile(self):
        self.user3.profile.website_url = WEBSITE_URL
        self.user3.profile.bio = BIO
        url = reverse("detail-profile", args=[self.user3.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['pk'], self.user3.pk)
        self.assertEqual(response.json()['username'], self.user3.username)
        self.assertEqual(response.json()['email'], self.user3.email)
