from django.urls import path
from posts.views import CreatePostView

urlpatterns = [
    path('create-post', CreatePostView.as_view(), name="create-post"),
]
