from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from Account .models import Follow, Profile
from posts.models import Like, Post
from Stories.models import Story
from .serializers import ProfileSerializer, PostSerializer, StorySerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from .serializers import PostSerializer

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Account.models import Profile, Follow
from posts.models import Post
from Stories.models import Story
from .serializers import ProfileSerializer, PostSerializer, StorySerializer

from .mypagination import myPagePagination


class HomeAPIView(ListAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    pagination_class = myPagePagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs): 
        # posts_response = super().list(request, *args, **kwargs)
        profile, _ = Profile.objects.get_or_create(user=request.user)
        # stories = Story.objects.all().order_by("-created_at")
        
        context = {
            "profile": ProfileSerializer(profile).data,
            # "stories": StorySerializer(stories, many=True).data,
            # "posts": posts_response.data,  
            "statistics": {
                "posts_count": Post.objects.filter(user=request.user).count(),
                "followers_count": Follow.objects.filter(following=request.user).count(),
                "following_count": Follow.objects.filter(follower=request.user).count(),
            }
        }
        return Response(context)

