from posts import views as posts_views      
from Account import views as account_views  
from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Post
from comments.forms import CommentForm
from .models import Comment
from django.contrib.auth.decorators import login_required

def comment_view(request, pk):  
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True) 
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')    
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                new_comment.parent = parent_comment 
            new_comment.save()
            return redirect('home')
    else:
        comment_form = CommentForm()
    return render(request, 'comments.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user == comment.author or request.user == comment.post.user:
        comment.delete()

    return redirect(request.META.get("HTTP_REFERER", "home"))