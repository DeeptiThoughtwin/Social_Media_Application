from posts import views as posts_views      
from Account import views as account_views  
from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Post
from comments.forms import CommentForm
from .models import Comment
from django.contrib.auth.decorators import login_required


def comment_view(request, pk):  
    """Display comments for a post and handle new comment submissions.

    Fetches a specific post by its primary key show all its active comments.
    If a POST request is received it verifies authentication validates the
    form data.
    handles optional nested threading replies using a parent IDand links the 
    new comment to both the post and the authenticated author.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): The primary key of the post associated with the comments.

    Returns:
        HttpResponseRedirect: Redirects to the login page if an unauthenticated user
            tries to post, or redirects to the 'home' view upon a successful comment 
            submission.

        HttpResponse: Renders the 'comments.html' template with the target post, its active 
            comments list, and an empty or invalid instance of CommentForm.
    """
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
    """Delete a specific comment if the user has the required permissions.

    Fetches the comment by its primary key. The operation executes successfully only
    if the requesting user is either the author of the comment or the owner of the 
    post where the comment was published.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): The primary key of the comment to be deleted.

    Returns:
        HttpResponseRedirect: Redirects back to the previous page using HTTP_REFERER.
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author or request.user == comment.post.user:
        comment.delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))
