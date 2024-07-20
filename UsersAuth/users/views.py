from .models import Upload, Follow
from .serializers import UserSerializer, UserPublicProfileRequestSerializer, UserPublicProfileResponseSerializer, UserFollowersSerializer, UserFollowingSerializer

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated



class RegisterView(APIView):
    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            user = User.objects.get(username=serializer.data['username'])

            return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        userprofile = user.userprofile
        serializer = UserPublicProfileResponseSerializer(userprofile)
        return Response({"username": user.username, "profile":serializer.data}, status=status.HTTP_200_OK)
    
    
    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        
        if request.user != user:
            return Response({"error": "You are not the owner."}, status=status.HTTP_403_FORBIDDEN)
        
        userprofile = user.userprofile
    
        serializer = UserPublicProfileRequestSerializer(userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            if 'picture' in request.FILES:
                picture = request.FILES['picture']
                public_uri = Upload.upload_image(picture, picture.name)
                serializer.validated_data['picture'] = public_uri

            serializer.save()
            data = UserPublicProfileResponseSerializer(userprofile).data
            return Response({"username": user.username, "profile":data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    
class FollowView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, username):
        follower = get_object_or_404(User, username=request.user.username)
        followed = get_object_or_404(User, username=username)
        follow, created = Follow.objects.get_or_create(follower=follower,followed=followed)
        
        if not created:
            return Response(f"Already following {follow.followed}, use DELETE to unfollow",status=status.HTTP_200_OK)
        
        return Response(f"Succesfully following {follow.followed}",status=status.HTTP_200_OK)
    
    
    def delete(self, request, username):
        follower = get_object_or_404(User, username=request.user.username)
        followed = get_object_or_404(User, username=username)
        follow = Follow.objects.filter(followed=followed).filter(follower=follower)
        
        return Response(f"Succesfully following {follow.user}",status=status.HTTP_200_OK)
    
    
class FollowersView(APIView):
    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    
    def get(self, request, username):
        user = User.objects.get(username=username)
        followers = Follow.objects.filter(followed=user)
        serializer = UserFollowersSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FollowingView(APIView):
    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]
    
    def get(self, request, username):
        user = User.objects.get(username=username)
        followings = Follow.objects.filter(follower=user)
        serializer = UserFollowingSerializer(followings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)