
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
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('profile')



@login_required
def like_post(request, post_id):
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
    post = get_object_or_404(Post, id=post_id)
    return render(request,"posts/post_detail.html",{"post": post})




