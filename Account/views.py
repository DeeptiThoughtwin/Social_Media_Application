from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Follow, Profile
from posts.models import Like, Post
from Stories.forms import StoryForm
from Stories.models import Story
from .forms import ProfileUpdateForm, UserUpdateForm,LoginForm,RegistrationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
import random

class HomeView(LoginRequiredMixin, View):
    """
    Display the home page for the authenticated user.
    Retrieves or creates the user's profile, fetches all posts and
    stories, checks follow and like status for each post, and calculates
    user statistics such as post count, followers count, and following
    count.
    """

    login_url = "login"

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for the home page.
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            HttpResponse: The rendered home page containing the user's
            profile, posts, stories, and account statistics.
        """
        profile, _ = Profile.objects.get_or_create(user=request.user)
        posts = Post.objects.all().order_by("-created_at")
        stories = Story.objects.all().order_by("-created_at")
        for post in posts:
            post.is_following = Follow.objects.filter(follower=request.user,following=post.user,).exists()
            post.is_liked = Like.objects.filter(user=request.user,post=post,).exists()
        context = {
            "profile": profile,
            "posts": posts,
            "posts_count": Post.objects.filter(user=request.user).count(),
            "followers_count": Follow.objects.filter(following=request.user).count(),
            "following_count": Follow.objects.filter(follower=request.user).count(),
            "stories": stories,
        }
        return render(request,"home.html",context)





class SignupView(View):
    """
    Handle user registration requests.
    Displays the registration form for GET requests and processes the
    submitted form for POST requests. If registration succeeds, the
    user is authenticated, logged in, and redirected to the home page.
    """

    def get(self, request, *args, **kwargs):
        """
        Display the registration form.
        Args:
            request (HttpRequest): The incoming HTTP request.
        Returns:
            HttpResponse: The rendered signup page.
        """
        form = RegistrationForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        Process the submitted registration form.
        Args:
            request (HttpRequest): The incoming HTTP request.
        Returns:
            HttpResponse: A redirect to the home page if registration
            succeeds; otherwise, the rendered form with validation errors.
        """
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request,username=username,password=password)
            if user is not None:
                auth_login(request, user)
            messages.success(request,f"Welcome {username}! Your account has been created.")
            return redirect("home")
        return render(request, "signup.html", {"form": form})




class LoginView(View):
    """
    Authenticate and log in a user.
    """
    def get(self, request, *args, **kwargs):
        """
        Display the login form.
        Returns:
            HttpResponse: The rendered login page.
        """
        if request.user.is_authenticated:
            return redirect("home")
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        Authenticate the submitted credentials.
        Returns:
            HttpResponse: Redirects to the home page on successful login
            or re-renders the login form with validation errors.
        """
        if request.user.is_authenticated:
            return redirect("home")
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
                )
            if user is not None:
                auth_login(request, user)
                messages.success(request,f"Welcome back {user.username}")
                return redirect("home")
        return render(request, "login.html", {"form": form})





class LogoutView(View):
    """
    Log out the authenticated user.
    Terminates the current user session, displays a success message,
    and redirects the user to the login page.
    """
    def get(self, request, *args, **kwargs):
        """
        Log out the current user.
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            HttpResponseRedirect: Redirects to the login page after
            successfully logging out the user.
        """
        auth_logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("login")




class ProfileView(LoginRequiredMixin, View):
    """
    Display the authenticated user's profile.
    Retrieves the user's profile information, posts, and account
    statistics, then renders the profile page.
    """
    login_url = "login"

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for the profile page.

        Retrieves or creates the user's profile, fetches the user's
        posts, determines the like status for each post, and calculates
        the follower, following, and post counts.
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            HttpResponse: The rendered profile page with the user's
            profile information and statistics.
        """
        profile, _ = Profile.objects.get_or_create(user=request.user)
        posts = Post.objects.filter(user=request.user).order_by("-created_at")
        for post in posts:
            post.is_liked = Like.objects.filter(user=request.user,post=post).exists()
        context = {
            "profile": profile,
            "posts": posts,
            "posts_count": posts.count(),
            "followers_count": Follow.objects.filter(following=request.user).count(),
            "following_count": Follow.objects.filter(follower=request.user).count(),
        }
        return render(request, "profile/profile.html", context)





class EditProfileView(LoginRequiredMixin, View):
    """
    Allow the authenticated user to update their profile information.
    Displays the profile editing forms for GET requests and processes
    the submitted forms for POST requests.
    """

    login_url = "login"

    def get(self, request, *args, **kwargs):
        """
        Display the profile editing forms.
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            HttpResponse: The rendered profile editing page.
        """
        profile, _ = Profile.objects.get_or_create(user=request.user)
        context = {
            "user_form": UserUpdateForm(instance=request.user),
            "profile_form": ProfileUpdateForm(instance=profile),
            "profile": profile,
        }
        return render(request, "profile/edit_profile.html", context)

    def post(self, request, *args, **kwargs):
        """
        Process the submitted profile update forms.
        Validates and saves both the user and profile forms. If both
        forms are valid, the user's profile is updated and the user is
        redirected to the profile page.
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            HttpResponse: A redirect to the profile page if the forms are
            valid; otherwise, the rendered editing page with validation
            errors.
        """
        profile, _ = Profile.objects.get_or_create(user=request.user)
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Profile updated successfully.")
            return redirect("profile")
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "profile": profile,
        }
        return render(request, "profile/edit_profile.html", context)






class DeleteProfileView(LoginRequiredMixin, View):
    """
    Permanently delete the authenticated user's account.
    Logs out the current user, deletes the associated user account,
    displays a success message, and redirects to the login page.
    """
    login_url = "login"
    def post(self, request, *args, **kwargs):
        """
        Delete the authenticated user's account.
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            HttpResponseRedirect: Redirects to the login page after
            successfully deleting the user account.
        """
        user = request.user
        auth_logout(request)
        user.delete()
        messages.success(request,"Your account has been permanently deleted.")
        return redirect("login")





class FollowUserView(LoginRequiredMixin, View):
    """
    Toggle the follow status for a user.
    Creates a follow relationship if one does not exist. Otherwise,
    removes the existing follow relationship.
    """
    login_url = "login"
    def post(self, request, user_id, *args, **kwargs):
        """
        Follow or unfollow the specified user.
        Args:
            request (HttpRequest): The incoming HTTP request.
            user_id (int): The ID of the user to follow or unfollow.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            JsonResponse: A JSON response containing the updated follow
            status and follower count.
        """
        user_to_follow = get_object_or_404(User, id=user_id)
        if request.user == user_to_follow:
            return JsonResponse({"error": "You cannot follow yourself."},status=400)
        follow, created = Follow.objects.get_or_create(follower=request.user,following=user_to_follow)
        if created:
            following = True
        else:
            follow.delete()
            following = False
        followers_count = Follow.objects.filter(following=user_to_follow).count()
        return JsonResponse(
            {
                "following": following,
                "followers_count": followers_count,
            }
        )



class FeedView(LoginRequiredMixin, View):
    """
    Display the user's feed.
    Retrieves all posts and stories ordered by creation date and
    initializes a form for creating a new story.
    """
    login_url = "login"
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for the feed page.
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            HttpResponse: The rendered home page containing posts,
            stories, and the story creation form.
        """
        posts = Post.objects.all().order_by("-created_at")
        stories = Story.objects.all().order_by("-created_at")
        story_form = StoryForm()
        context = {
            "posts": posts,
            "stories": stories,
            "story_form": story_form,
        }
        return render(request, "home.html", context)




class NewCommentView(LoginRequiredMixin, View):
    """
    Display the new comment page.
    """
    login_url = "login"
    def get(self, request, *args, **kwargs):
        """
        Render the new comment page.
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            HttpResponse: The rendered new comment page.
        """
        return render(request, "newcomments.html")

    


class ForgotPasswordView(View):
    """
    Handle password reset requests.

    Displays the forgot password form and sends an OTP to the
    registered email address if a matching user exists.
    """
    def get(self, request, *args, **kwargs):
        """
        Display the forgot password form.
        Returns:
            HttpResponse: The rendered forgot password page.
        """
        form = ForgotPasswordForm()
        return render(request,"password/forgot_password.html",{"form": form})

    def post(self, request, *args, **kwargs):
        """
        Process the forgot password form.
        Generates and emails an OTP for password reset if the
        provided email belongs to a registered user.
        Returns:
            HttpResponse: Redirects to OTP verification on success,
            otherwise re-renders the form.
        """
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                otp = str(random.randint(100000, 999999))
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
                return redirect("verify_otp")
        return render(request,"password/forgot_password.html",{"form": form})




class VerifyOTPView(View):
    """
    Verify the OTP submitted by the user.
    """
    def get(self, request, *args, **kwargs):
        """
        Display the OTP verification form.
        Returns:
            HttpResponse: The rendered OTP verification page.
        """
        if not request.session.get("reset_user"):
            return redirect("forgot_password")
        form = OTPForm()
        return render(request,"password/verify_otp.html",{"form": form})

    def post(self, request, *args, **kwargs):
        """
        Validate the submitted OTP.
        Returns:
            HttpResponse: Redirects to the password reset page if
            the OTP is valid; otherwise, re-renders the form with
            validation errors.
        """
        user_id = request.session.get("reset_user")
        if not user_id:
            return redirect("forgot_password")
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            otp_obj = PasswordResetOTP.objects.filter(user_id=user_id,otp=otp).first()
            if otp_obj:
                return redirect("reset_password")
            form.add_error("otp","OTP you entered is incorrect or expired.")
        return render(request,"password/verify_otp.html",{"form": form})




class ResetPasswordView(View):
    """
    Reset the user's password after successful OTP verification.
    """
    def get(self, request, *args, **kwargs):
        """
        Display the password reset form.
        Returns:
            HttpResponse: The rendered password reset page.
        """
        if not request.session.get("reset_user"):
            return redirect("forgot_password")
        form = ResetPasswordForm()
        return render(request,"password/reset_password.html",{"form": form})

    def post(self, request, *args, **kwargs):
        """
        Update the user's password.
        Returns:
            HttpResponse: Redirects to the home page after
            successfully resetting the password.
        """
        user_id = request.session.get("reset_user")
        if not user_id:
            return redirect("forgot_password")
        user = User.objects.get(id=user_id)
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["password1"])
            user.save()
            PasswordResetOTP.objects.filter(user=user).delete()
            del request.session["reset_user"]
            return redirect("home")
        return render(request,"password/reset_password.html",{"form": form})
