from django.test import TestCase

# Models
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class UserProfileTests(TestCase):
    def setUp(self):
        print("Profile Test Begin")
        self.user = get_user_model().objects.create_user(
            username='testuser100',
            email='testuser100@email.com',
            password='testpass123'
        )
        
    def test_profile(self):
        self.assertEqual(self.user.username, 'testuser100')
        self.assertEqual(self.user.email, 'testuser100@email.com')
        self.assertTrue(self.user.profile)
        self.assertTrue(Token.objects.filter(user=self.user).exists())