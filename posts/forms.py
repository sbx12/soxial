from django.forms import ModelForm
from django import forms

from posts.models import Post

class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['user', 'description', 'image']
