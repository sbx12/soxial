from django.urls import path

from posts.api import views

urlpatterns = [
    path('', views.PostList.as_view(), name="list-posts"),
    path('public/<int:pk>', views.PostPublicProfileList.as_view(), name="public-list-posts"),
    path('user', views.PostProfileList.as_view(), name="list-user-posts"),
    path('create', views.PostCreate.as_view(), name="create-posts"),
    path('<int:pk>/', views.PostDetail.as_view(), name="detail-posts"),
    path('<int:pk>/powerup', views.PostPowerup.as_view(), name="powerup-posts"),
    
    path('comment', views.CommentCreate.as_view(), name="create-comment"),
    path('comment/<int:pk>/', views.CommentDetail.as_view(), name="detail-comment"),
    path('comment/<int:pk>/powerup', views.CommentPowerup.as_view(), name="powerup-comment"),
]