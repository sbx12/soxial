from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

# Models
from django.contrib.auth import get_user_model
from posts.models import Post, Comment

IMAGE_URL = "M:\Coding\Django\Soxial\soxial\soxial\media\profile\images\Kidrobot.jpeg"

class PostTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser100",
            email="testuser100@email.com",
            password="testpass123"
        )
        
        self.user2 = get_user_model().objects.create_user(
            username="testuser200",
            email="testuser200@email.com",
            password="testpass123"
        )
        
        self.test_image = SimpleUploadedFile(name='test_image.jpg', content=open(IMAGE_URL, 'rb').read(), content_type='image/jpeg')
        self.post = Post.objects.create(
            user=self.user,
            description="lorem ep sum",
            image=self.test_image,
        )
        self.post.tag.set([self.user2])
        self.post.power_up.set([self.user, self.user2])
        
        self.comment = Comment.objects.create(
            user=self.user2,
            post=self.post,
            comment="lorem ep sum",
        )
        self.comment.power_up.set([self.user, self.user2])
    
    def test_post(self):
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(f'{self.post.description}', 'lorem ep sum')
        self.assertTrue(self.post.image)
        print(self.post.image)
        self.assertEqual(self.post.power_up.count(), 2)
        self.assertEqual(self.post.tag.count(), 1)
        self.assertEqual(self.post.comment_set.count(), 1)
        
    def test_comment(self):
        self.assertEqual(self.comment.user, self.user2)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(f'{self.comment.comment}', 'lorem ep sum')
        self.assertEqual(self.post.power_up.count(), 2)