from django.urls import path
from Account.api.views import (HomeAPIView,SignupAPIView,LoginAPIView,
LogoutAPIView,ProfileAPIView,FeedAPIView,DeleteProfileAPIView,
FollowUserAPIView,ResetPasswordAPIView,ForgotPasswordAPIView,
VerifyOTPAPIView,CommentAPIView,EditProfileAPIView)


urlpatterns = [
    path("home/", HomeAPIView.as_view(), name="home"),
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),

    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("profile/edit/",EditProfileAPIView.as_view(),name="edit-profile"),
    path("profile/delete/",DeleteProfileAPIView.as_view(),name="delete-profile"),

    path("follow/<int:user_id>/",FollowUserAPIView.as_view(),name="follow-user"),
    path("feed/",FeedAPIView.as_view(),name="feed"),
    path("posts/<int:post_id>/comments/",CommentAPIView.as_view(),name="comments"),

    path("forgot-password/",ForgotPasswordAPIView.as_view(),name="forgot-password"),
    path("verify-otp/",VerifyOTPAPIView.as_view(),name="verify-otp"),
    path("reset-password/",ResetPasswordAPIView.as_view(),name="reset-password"),
]

