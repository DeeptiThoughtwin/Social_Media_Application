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
from .forms import RegistrationForm,LoginForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.models import User
from django.http import JsonResponse






@login_required
def home(request):
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
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request,f"Welcome {username}! Your account has been created.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request,"signup.html",{"form": form})




def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request,username=username,password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request,f"Welcome back {user.username}")
                return redirect("home")
    else:
        form = LoginForm()
    return render(request,"login.html",{"form": form})




@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login") 




@login_required
def profile(request):
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





from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

@login_required
@require_POST
def delete_profile(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "Your account has been permanently deleted.")
    return redirect('login')  




@login_required
def follow_user(request, user_id):
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
    posts = Post.objects.all().order_by("-created_at")
    stories = Story.objects.all().order_by("-created_at") 
    story_form = StoryForm()

    # print(stories)

    return render(request, "home.html", {
        "posts": posts,
        "stories": stories,
        "story_form": story_form,
    })



def new_comment(request):
    return render(request,'newcomments.html')


