from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Follow
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    
    
class UserPublicProfileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'description', 'picture']

    picture = serializers.ImageField(required=False)


class UserPublicProfileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'description', 'picture']

    picture = serializers.URLField(required=False)
    
    
class UserFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['username']
        
    username = serializers.CharField(source='follower.username')
    
class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['username']
        
    username = serializers.CharField(source='followed.username')