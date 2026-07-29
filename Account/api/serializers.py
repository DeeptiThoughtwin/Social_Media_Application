from rest_framework import serializers
from Account.models import Profile,Profile,Follow
from Stories.models import Story
from posts.models import Post
from comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from comments.models import Comment

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_is_following(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return user.following.filter(following=obj.user).exists()

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.like_set.filter(user=user).exists()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username","email","password","confirm_password","first_name","last_name",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            password=validated_data["password"],
        )
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError(
                "Invalid username or password."
            )
        attrs["user"] = user
        return attrs



class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.likes.count() 




class ProfileSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id","user","bio","profile_picture","posts","posts_count","followers_count","following_count",
        ]

    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj.user).order_by("-created_at")
        return PostSerializer(posts, many=True).data

    def get_posts_count(self, obj):
        return Post.objects.filter(user=obj.user).count()

    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj.user).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj.user).count()




class EditProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = [
            "first_name","last_name","email","bio","profile_picture",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)
        user.save()
        instance.bio = validated_data.get("bio", instance.bio)
        instance.profile_picture = validated_data.get(
            "profile_picture",
            instance.profile_picture
        )
        instance.save()
        return instance



class FollowSerializer(serializers.Serializer):
    following = serializers.BooleanField()
    followers_count = serializers.IntegerField()




class FeedPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"


class FeedStorySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Story
        fields = "__all__"





class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="author.username",   # Fixed: Changed user to author
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id","author","username","post","body","created_on","active","parent",              
        ]
        read_only_fields = [
            "author"                
        ]



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=8
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8
    )

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password2": "Passwords do not match."
                }
            )

        return attrs
