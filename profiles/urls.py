from django.urls import path
from profiles import views

urlpatterns = [
    path('', views.ProfileView.as_view(), name="profile"),
    path('<int:pk>', views.PublicProfileView.as_view(), name="public-profile"),
]
