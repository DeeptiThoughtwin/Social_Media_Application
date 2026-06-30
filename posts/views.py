from django.shortcuts import render, redirect,get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post, PostMedia, Like, Comment
from Account.models import Follow



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
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'posts/create_posts.html', {'form': form})




def feed(request):
    posts = Post.objects.all().order_by("-created_at")
    for post in posts:
        post.is_following = Follow.objects.filter(follower=request.user,following=post.user).exists()
    return render(request, "posts/feed.html", {"posts": posts})

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
    return redirect('profile')



    # @login_required
    # def add_comment(request, post_id):

    #     post = get_object_or_404(Post, id=post_id)

    #     if request.method == "POST":
    #         text = request.POST.get("text")

    #         if text:
    #             Comment.objects.create(
    #                 user=request.user,
    #                 post=post,
    #                 text=text
    #             )

    #     return redirect("post_detail", post_id=post.id)




@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request,"posts/post_detail.html",{"post": post})
