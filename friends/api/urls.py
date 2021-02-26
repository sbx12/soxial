from django.urls import path

from friends.api import views

urlpatterns = [
    path('', views.FriendList.as_view(), name="list-friends"),
    path('friend-request/recieved', views.FriendRequestList.as_view(), name="list-friend-request"),
    path('friend-request/sent', views.FriendSentRequestList.as_view(), name="list-friend-sent-request"),
    path('friend-request/create', views.FriendSentRequestCreate.as_view(), name="create-friend-request"),
    path('friend-request/<int:pk>/', views.FriendRequestDetail.as_view(), name="detail-friend-request"),
]