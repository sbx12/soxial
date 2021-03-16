from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

# Models
from django.contrib.auth import get_user_model
from posts.models import Post, Comment

IMAGE_URL = "YOURIMAGELINKHERE"
DESCRIPTION = "lorem ep sum"
COMMENT = "lorem ep sum"


class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Posts Test Begin")
        # Create User1
        cls.user = get_user_model().objects.create_user(
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
        # Create Post        
        self.test_image = SimpleUploadedFile(name='test_image.jpg', content=open(IMAGE_URL, 'rb').read(), content_type='image/jpeg')
        self.post = Post.objects.create(
            user=self.user,
            description=DESCRIPTION,
            image=self.test_image,
        )
        self.post.people_tag.set([self.user2])
        self.post.powerup.set([self.user, self.user2])
        
        # Create Comment
        self.comment = Comment.objects.create(
            user=self.user2,
            post=self.post,
            comment=COMMENT,
        )
        self.comment.powerup.set([self.user, self.user2])
    
    def test_post(self):
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(f'{self.post.description}', DESCRIPTION)
        self.assertTrue(self.post.image)
        self.assertEqual(self.post.powerup.count(), 2)
        self.assertEqual(self.post.people_tag.count(), 1)
        self.assertEqual(self.post.comment_set.count(), 1)
        
    def test_comment(self):
        self.assertEqual(self.comment.user, self.user2)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(f'{self.comment.comment}', COMMENT)
        self.assertEqual(self.post.powerup.count(), 2)