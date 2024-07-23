from django.urls import path

from .views import RegisterView, ProfileView, FollowView, FollowersView, FollowingView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('profile/<str:username>', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/follow', FollowView.as_view(), name='follow'),
    path('profile/<str:username>/followers', FollowersView.as_view(), name='followers'),
    path('profile/<str:username>/following', FollowingView.as_view(), name='following'),
]