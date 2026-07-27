from rest_framework import serializers
from django.contrib.auth.models import User
from Account.models import Profile
from posts.models import Post
from Stories.models import Story

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 

    class Meta:
        model = Profile
        fields = ['user'] 


class StorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'user', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_following = serializers.BooleanField(read_only=True) 
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'created_at', 'is_following', 'is_liked']
