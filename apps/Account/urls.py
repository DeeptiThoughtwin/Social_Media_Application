
from django.urls import path
from django.contrib.auth import views as auth_views
from apps.Account import views
from apps.posts import views as post_view


urlpatterns = [

    path("signup/", views.SignupView.as_view(), name="signup"),
    path("", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    
    path("newcomments/", views.NewCommentView.as_view(), name="new_comment"),
    path("home/", views.HomeView.as_view(), name="home"),

    

    path('<int:post_id>/',post_view.PostDetailView.as_view(), name='post_detail'),
    path("follow/<int:user_id>/",views.FollowUserView.as_view(),name="follow_user"),

    

    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("edit-profile/",views.EditProfileView.as_view(),name="edit_profile"),
    path('profile/delete/',views.DeleteProfileView.as_view(), name='delete_profile'),

   


    path("forgot-password/",views.ForgotPasswordView.as_view(),name="forgot_password"),
    path("verify-otp/",views.VerifyOTPView.as_view(),name="verify_otp"),
    path("reset-password/",views.ResetPasswordView.as_view(),name="reset_password"),

    
]


