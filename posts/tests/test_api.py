import json
import tempfile

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Tag

# Serialzer
from posts.api.serializers import PostSerializer

IMAGE_URL = "M:\Coding\Django\Soxial\soxial\soxial\media\profile\images\Kidrobot.jpeg"
MOCK_IMAGE = tempfile.NamedTemporaryFile(suffix=".jpg").name
DESCRIPTION = "lorem ep sum"
DESCRIPTION2 = "Xorem sp uum"
COMMENT = "lorem ep sum"

class PostAPITest(APITestCase):
    
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
        
        # Create User3
        cls.user3 = get_user_model().objects.create_user(
            username='testuser300',
            email='testuser300@email.com',
            password='testpass123'
        )
        
        cls.tag1 = Tag.objects.create(
            name="hashtag",
        )
        
        cls.test_image = SimpleUploadedFile(name='test_image.jpg', content=open(IMAGE_URL, 'rb').read(), content_type='image/jpeg')
        
    def setUp(self):
        # Create Post     
        self.post = Post.objects.create(
            user=self.user1,
            description=DESCRIPTION,
            image=MOCK_IMAGE,
        )
        self.post.powerup.set([self.user1, self.user2])
        self.post.people_tag.set([self.user2])
        
        # Create Comment
        self.comment = Comment.objects.create(
            user=self.user1,
            post=self.post,
            comment="lorem",
        )
        self.comment.powerup.set([self.user1])
                
        # Auth
        self.api_authentication()
        
    def api_authentication(self):
        # Setup Auth
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user1.auth_token.key)
        
    def test_list_post(self):
        url = reverse("list-posts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_post(self):
        url = reverse("detail-posts", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['user']['pk'], self.user1.id)
        self.assertEqual(response.json()['description'], DESCRIPTION)
        self.assertEqual(response.json()['powerup'][0]['id'], self.user1.id)
        self.assertEqual(response.json()['people_tag'][0]['id'], self.user2.id)
        print(response.json()['image'])
        
    def test_put_post(self):
        # NOW UPDATE OBJECT
        url = reverse("detail-posts", kwargs={"pk": 1})
        data = {
            "user": self.user1.pk,
            "description": DESCRIPTION2,
            "tag": [],
            "people_tag": [self.user2.pk]
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], DESCRIPTION2)
        self.assertEqual(response.json()['people_tag'][0], self.user2.pk)
        
    def test_delete_post(self):
        url = reverse("detail-posts", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Post.objects.get_posts().filter(id=self.post.pk).exists())

    def test_create_post(self):
        url = reverse("create-posts")
        data = {
            "user": self.user1.pk,
            "description": DESCRIPTION,
            "people_tag": [self.user2.pk]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_powerup_add_post(self):
        url = reverse("powerup-posts", args=[self.post.pk])
        data = {
            "powerup": True,
            "user": self.user3.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.post.powerup.filter(id=self.user3.pk).exists())
        
    def test_powerup_remove_post(self):
        url = reverse("powerup-posts", args=[self.post.pk])
        data = {
            "powerup": False,
            "user": self.user1.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.post.powerup.filter(id=self.user1.pk).exists())
        
    # TEST COMMENT        
    def test_create_comment(self):
        url = reverse("create-comment")
        data = {
            "user": self.user1.pk,
            "post": self.post.pk,
            "comment": COMMENT
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['user'], self.user1.pk)
        self.assertEqual(response.json()['post'], self.post.pk)
        self.assertEqual(response.json()['comment'], COMMENT)
        
    def test_update_comment(self):
        url = reverse("detail-comment", args=[self.comment.pk] )
        data = {
            "user": self.user1.pk,
            "post": self.post.pk,
            "comment": COMMENT
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['comment'], COMMENT)
        
    def test_delete_comment(self):
        url = reverse("detail-comment", args=[self.comment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Comment.objects.filter(id=self.comment.pk).exists())
        
    def test_powerup_add_comment(self):
        url = reverse("powerup-comment", args=[self.comment.pk])
        data = {
            "powerup": True,
            "user": self.user3.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.comment.powerup.filter(id=self.user3.pk).exists())
        
    def test_powerup_remove_comment(self):
        url = reverse("powerup-comment", args=[self.comment.pk])
        data = {
            "powerup": False,
            "user": self.user1.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.comment.powerup.filter(id=self.user1.pk).exists())