from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post, PostMedia, Like
from Account.models import Follow
from Stories.models import Story
from Stories.forms import StoryForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse




@login_required
def create_post(request):
    """Create a new post  with its associated media files.

    Processes form data on POST requests attaches the post to the authenticated 
    user and loops through any uploaded files to detect and assign their media type 
    image or video before saving them to the database.

    Args:
        request (HttpRequest): The incoming HTTP request containing form and file data.

    Returns:
        HttpResponseRedirect: Redirects to the 'profile' view on successful creation.
        HttpResponse: Renders the 'postsor create_posts.html' template with the form context.
    """
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            files = request.FILES.getlist('files')
            for f in files:
                media_type = 'video' if f.content_type.startswith('video') else 'image'
                PostMedia.objects.create(post=post,file=f,media_type=media_type)
            return redirect('profile')
    else:
        form = PostForm()
    return render(request, 'posts/create_posts.html', {'form': form})



@login_required
def delete_post(request, post_id):
    """Delete a specific post owned by the current authenticated user.

    Fetches the target post ensuring that it belongs strictly to the requesting user.
    If the post exists and the user owns it the post is permanently deleted.

    Args:
        request (HttpRequest): The incoming HTTP request.
        post_id (int): The primary key identifier of the post to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the user's 'profile' page.
    """
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('profile')



@login_required
def like_post(request, post_id):
    """Toggle a like on a post and return the updated state via JSON.

    Checks if a like already exists for the given post.
    If it exists the like is turned into unliked.
    If it does not exist, a new like is recorded.

    Args:
        request (HttpRequest): The incoming HTTP request.
        post_id (int): The primary key identifier of the post being liked or unliked.

    Returns:
        JsonResponse: A JSON response containing the boolean 'liked' status 
            and the updated integer 'likes_count'.
    """
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user,post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({"liked": liked,"likes_count": post.likes.count()})



@login_required
def post_detail(request, post_id):
    """Render a dedicated detail page for a single post.

    Fetches the requested post by its primary key from the database and delivers 
    it to the detail template view.

    Args:
        request (HttpRequest): The incoming HTTP request.
        post_id (int): The primary key identifier of the post to display.

    Returns:
        HttpResponse: Renders the 'posts/post_detail.html' template with the post context.
    """
    post = get_object_or_404(Post, id=post_id)
    return render(request,"posts/post_detail.html",{"post": post})



@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.user:
        return redirect("home")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit_post.html", {
        "form": form,
        "post": post,
    })