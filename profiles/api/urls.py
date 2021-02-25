from django.urls import path

from profiles.api import views

urlpatterns = [
    path('<int:pk>/', views.UserProfileDetail.as_view(), name="detail-profile"),
]