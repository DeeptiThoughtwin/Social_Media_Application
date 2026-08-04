from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.Account.models import Profile, Follow,PasswordResetOTP,PasswordResetOTP,PasswordResetOTP
from apps.posts.models import Post
from apps.Stories.models import Story
from apps.Account.api.serializers import (
    LoginSerializer,
    ProfileSerializer,
    PostSerializer,
    StorySerializer,
    FollowSerializer,EditProfileSerializer,ResetPasswordSerializer,
    ProfileSerializer,RegistrationSerializer,CommentSerializer,FeedPostSerializer,
    FeedStorySerializer,LoginSerializer,ForgotPasswordSerializer,OTPSerializer
    )
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.contrib.auth import login
from apps.comments.models import Comment
import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken  
from apps.Account.api.throttles import LoginThrottle
from django.core.cache import cache


class HomeAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")

    def list(self, request, *args, **kwargs):
        profile, _ = Profile.objects.get_or_create(user=request.user)

        if posts_data is None:
            print("Cache Miss")
            posts = self.get_queryset()
            posts_data = self.get_serializer(
                posts,
                many=True,
                context={"request": request},
            ).data
            cache.set("home_posts", posts_data, timeout=300)
        else:
            print("Cache Hit")

        stories = Story.objects.all().order_by("-created_at")
        story_serializer = StorySerializer(stories, many=True)
        profile_serializer = ProfileSerializer(profile)
        return Response({
            "profile": profile_serializer.data,
            "posts": posts_data,
            "stories": story_serializer.data,
            "posts_count": Post.objects.filter(user=request.user).count(),
            "followers_count": Follow.objects.filter(following=request.user).count(),
            "following_count": Follow.objects.filter(follower=request.user).count(),
        })







class SignupAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    authentication_classes = [] 
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "Account created successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )








class LoginAPIView(APIView):
    """
    API View to authenticate users and return JWT access and refresh tokens.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    throttle_classes = [ LoginThrottle]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Both username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_active:
                return Response(
                    {"error": "This account has been deactivated."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful.",
                    "access": str(refresh.access_token),  
                    "refresh": str(refresh),  
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )






class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required to log out."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logged out successfully."},
                status=status.HTTP_200_OK,
            )
        except TokenError:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST
            )




class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        return profile





class EditProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = EditProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        return profile




class DeleteProfileAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        logout(request)
        user.delete()
        return Response(
            {
                "message": "Your account has been permanently deleted."
            },
            status=status.HTTP_204_NO_CONTENT,
        )




class FollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(
            User,
            id=user_id
        )
        if request.user == user_to_follow:
            return Response(
                {
                    "error": "You cannot follow yourself."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        follow, created = Follow.objects.get_or_create(follower=request.user,following=user_to_follow)
        if created:
            following = True
        else:
            follow.delete()
            following = False

        followers_count = Follow.objects.filter(following=user_to_follow).count()
        data = {
            "following": following,
            "followers_count": followers_count,
        }
        serializer = FollowSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )





class FeedAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedPostSerializer

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-created_at")
        stories = Story.objects.all().order_by("-created_at")
        post_serializer = FeedPostSerializer(posts,many=True)
        story_serializer = FeedStorySerializer(stories,many=True)
        return Response(
            {
                "posts": post_serializer.data,
                "stories": story_serializer.data,
            }
        )



class CommentAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )




class ForgotPasswordAPIView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {
                    "error": "User with this email does not exist."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        otp = str(
            random.randint(
                100000,
                999999
            )
        )
        PasswordResetOTP.objects.filter(user=user).delete()
        PasswordResetOTP.objects.create(user=user,otp=otp)
        send_mail(
            "OTP Verification",
            f"Your OTP code is: {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        request.session["reset_user"] = user.id
        return Response(
            {
                "message": "OTP sent successfully."
            },
            status=status.HTTP_200_OK
        )





class VerifyOTPAPIView(APIView):
    serializer_class = OTPSerializer

    def post(self, request):
        user_id = request.session.get("reset_user")
        if not user_id:
            return Response(
                {
                    "error": "Please request password reset first."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data["otp"]
        otp_obj = PasswordResetOTP.objects.filter(user_id=user_id,otp=otp).first()
        if not otp_obj:
            return Response(
                {
                    "error": "OTP is incorrect or expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        request.session["otp_verified"] = True
        return Response(
            {
                "message": "OTP verified successfully."
            },
            status=status.HTTP_200_OK
        )



class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        user_id = request.session.get("reset_user")
        otp_verified = request.session.get("otp_verified")
        if not user_id or not otp_verified:
            return Response(
                {
                    "error": "OTP verification required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=user_id)
        user.set_password(serializer.validated_data["password1"])
        user.save()
        PasswordResetOTP.objects.filter(user=user).delete()
        request.session.pop("reset_user",None)
        request.session.pop("otp_verified",None)
        return Response(
            {
                "message": "Password reset successfully."
            },
            status=status.HTTP_200_OK
        )
