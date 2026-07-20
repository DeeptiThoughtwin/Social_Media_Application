
from django.urls import path
from django.contrib.auth import views as auth_views
from Account import views
from posts import views as post_view

urlpatterns = [

    path("signup/",views.signup,name="signup"),
    path("",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
    
    path("newcomments/",views.new_comment, name="new_comment"),
    path("home/",views.home,name="home"),
    


    path('<int:post_id>/', post_view.post_detail, name='post_detail'),

    path("follow/<int:user_id>/",views.follow_user,name="follow_user"),
  

    path("profile/",views.profile,name="profile"),
    path("edit-profile/",views.edit_profile,name="edit_profile"),
    path('profile/delete/', views.delete_profile, name='delete_profile'),


   

    # path("password_reset/",auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),name="password_reset"),
    # path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name="password_reset_done"),
    # path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),name="password_reset_confirm"),
    # path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name="password_reset_complete"),




    path("forgot-password/",views.forgot_password,name="forgot_password"),
    path("verify-otp/",views.verify_otp,name="verify_otp"),
    path("reset-password/",views.reset_password,name="reset_password"),

    
]




