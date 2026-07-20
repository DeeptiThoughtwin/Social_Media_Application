from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Profile,Follow
from posts.models import Post,Like
from Stories.models import Story
from Stories.forms import StoryForm
from .forms import RegistrationForm,LoginForm,UserUpdateForm,ProfileUpdateForm,ResetPasswordForm
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
from django.core.mail import send_mail
from .models import PasswordResetOTP
from .forms import ForgotPasswordForm
from .forms import OTPForm
from .models import PasswordResetOTP
from django.conf import settings







@login_required
def home(request):
    """
    Display the home page for the logged -in user
    => Retrives or creates the logged-in user's profile.
    => fetches all posts and stories ordered by creation date.
    => check the current user follows each post's author.
    => check the current user has liked each post.
    => calculates the user's post count,follower count and following count.
    => passes all required data to the "home.html" template.

    Args:
        request(httprequest):the incoming http request.

        returns:
            httpResponse:Rendered home page with profile,posts,stories and user statistics.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.all().order_by("-created_at")
    stories = Story.objects.all().order_by("-created_at")
    for post in posts:
        post.is_following = Follow.objects.filter(
            follower=request.user,
            following=post.user
        ).exists()

        post.is_liked = Like.objects.filter(
            user=request.user,
            post=post
        ).exists()
    context = {
        "profile": profile,
        "posts": posts,
        "posts_count": Post.objects.filter(user=request.user).count(),
        "followers_count": Follow.objects.filter(following=request.user).count(),
        "following_count": Follow.objects.filter(follower=request.user).count(),
        "stories": stories,
    }
    return render(request, "home.html", context)

def signup(request):
    """
    handling user registration

    displays the registration for get requests and processes the submitted form for post 
    requests. If the form is valid a new user account is created a success msg is displayed
    and the user is redirected to the login page.

    Args:
    request(httprequest):incomming http request

    return: 
        httpresponse: renders the signup page or redirects to the login page after successful 
        registration.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                auth_login(request, user)
            messages.success(
                request,
                f"Welcome {username}! Your account has been created."
            )
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "signup.html", {"form": form})



def login(request):
    """Handle user authentication and login requests.

    If a user is already authenticated they are redirected to the home page.
    For a POST request the submitted login credentials are validated, the 
    user is authenticated, and a success message is flashed upon a successful 
    login. For a GET request, an empty login form is presented.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A redirect to the 'home' view if the user is already 
            authenticated or loggedin successfully. Otherwise, returns a rendered 
            HTML response containing the 'login.html'.
    """

    # 1. First, check if the user is already logged in
    if request.user.is_authenticated:
        return redirect("home")
        
    # 2. If they are NOT logged in, handle the form processing (Notice the shift to the left)
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back {user.username}")
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})





@login_required
def logout(request):
    """Log out the current authenticated user.

    Clears the active session data, displays a successful logout msg.
    and routes the unauthenticated user back to the login screen.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponseRedirect: A redirect response targeting the 'login' URL.
    """
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login") 




@login_required
def profile(request):
    """Display the authenticated user's profile dashboard.

    Retrieves or create user's profile record fetches all of their 
     posts, evaluates like states for each post, and total
      followers, following counts, and posts.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A rendered HTML response loading the 'profile/profile.html' 
            template.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(user=request.user).order_by("-created_at")
    for post in posts:
        post.is_liked = Like.objects.filter(
            user=request.user,
            post=post
        ).exists()
    followers_count = Follow.objects.filter(
        following=request.user).count()
    following_count = Follow.objects.filter(
        follower=request.user).count()

    context = {
        "profile": profile,
        "posts": posts,
        "posts_count": posts.count(),
        "followers_count": followers_count,
        "following_count": following_count,
    }

    return render(request, "profile/profile.html", context)


@login_required
def edit_profile(request):
    """Handle the modification of user profile data.
    Fetches or creates the user's Profile record.
    For a POST request, processes and validates both the user details
    For a GET request, initializes both formspre-populated with the current user and profile instances.
    Args:
        request (HttpRequest): The incoming HTTP request .
    Returns:
        HttpResponse: A redirect to the 'profile' view upon a successful form submission, or a rendered HTML response showcasing the multi-form editing template with context variables.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        # import pdb;pdb.set_trace()
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        # print("User Errors:", user_form.errors)
        # print("Profile Errors:", profile_form.errors)
        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Profile updated successfully.")
            return redirect("profile")
        print("user_form: ",user_form)
        print("profile_form: ",profile_form)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        
    return render(request,"profile/edit_profile.html",{"user_form": user_form,"profile_form": profile_form,"profile": profile})




@login_required
def delete_profile(request):
    """Permanently delete the authenticated user's account.

    target the current user instance terminates their active authenticated 
    session, removes their user record from the database  with cascading data.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponseRedirect: A redirect response targeting the 'login' URL.
    """
    user = request.user
    auth_logout(request) 
    user.delete()
    messages.success(request, "Your account has been permanently deleted.")
    return redirect('login')  



@login_required
def follow_user(request, user_id):
    """Toggle the follow state between the active user and a target user.

    Validates that the target user exists and that the user is not attempting to 
    follow themselves. If a relationship record does not exist, it creates one 
    follow; if it already exists, it removes it unfollow.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (int): The unique identifier of the target user to follow or unfollow.

    Returns:
        JsonResponse: A JSON response object containing the updated relationship boolean 
        'following' and the total updated follower 'followers_count' for the target user.
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user == user_to_follow:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)
    follow, created = Follow.objects.get_or_create(follower=request.user,following=user_to_follow)
    if created:
        following = True
    else:
        follow.delete()
        following = False
    followers_count = Follow.objects.filter(
        following=user_to_follow
    ).count()
    return JsonResponse({"following": following, "followers_count": followers_count})


@login_required
def feed(request):
    """Fetch and display all posts and stories for the feed page.

    Queries all existing   posts and user stories from the database,
    ordering them from newest to oldest, and initializes an empty form
    for creating a new story.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A rendered 'home.html' page populated with context data 
            containing posts, stories, and the story form.
    """
    posts = Post.objects.all().order_by("-created_at")
    stories = Story.objects.all().order_by("-created_at") 
    story_form = StoryForm()

    # print(stories)

    return render(request, "home.html", {
        "posts": posts,
        "stories": stories,
        "story_form": story_form,
    })



@login_required
def new_comment(request):
    """Render the comment creation page or process a new comment submission.
    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered 'newcomments.html' template.
    """
    return render(request, 'newcomments.html')
    





def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # print("Entered Email:", email)
            # print("User:", user)
            user = User.objects.filter(email=email).first()
            if user:
                request.session["reset_user"] = user.id
                otp = str(random.randint(100000,999999))
                PasswordResetOTP.objects.filter(user=user).delete()
                PasswordResetOTP.objects.create(
                    user=user,
                    otp=otp
                )
                # print("Checking email:", settings.EMAIL_HOST_USER)
                # print("Checking password length:", len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else "None")
                
                user_email = request.POST.get('email') 
                send_mail(
                'OTP Verification',                 
                f'Your OTP code is: {otp}',         
                settings.DEFAULT_FROM_EMAIL,          
                [user.email],                
                fail_silently=False,
            )

                request.session["reset_user"] = user.id
                return redirect("verify_otp")
    else:
        form = ForgotPasswordForm()
    return render(request,"password/forgot_password.html",{"form":form})





def verify_otp(request):
    user_id = request.session.get("reset_user")
    if not user_id:
        return redirect("password/forgot_password")
    if request.method=="POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            otp_obj = PasswordResetOTP.objects.filter(
                user_id=user_id,
                otp=otp
            ).first()

            if otp_obj:
                return redirect("reset_password")

            else:
                form.add_error("otp", "OTP you entered is incorrect or expired.")
    else:
        form=OTPForm()
    return render(request,"password/verify_otp.html",{"form":form})




 





def reset_password(request):
    user_id = request.session.get("reset_user")
    if not user_id:
        return redirect("forgot_password")
    user = User.objects.get(id=user_id)
    if request.method=="POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(
                form.cleaned_data["password1"]
            )
            user.save()
            PasswordResetOTP.objects.filter(user=user).delete()
            del request.session["reset_user"]
            return redirect("home")
    else:
        form=ResetPasswordForm()
    return render(request,"password/reset_password.html",{"form":form})