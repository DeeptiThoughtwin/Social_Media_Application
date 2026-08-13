from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.posts.models import Post
from apps.comments.forms import CommentForm
from apps.comments.models import Comment
import logging
logger = logging.getLogger(__name__)


class CommentView(View):
    """Display comments for a post and handle new comment submissions."""
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        logger.info(
            "Comments page viewed: post_id=%s user_id=%s",
            post.id,
            request.user.id if request.user.is_authenticated else None,
        )
        return render(request,
            "comments.html",
            {
                "post": post,
                "comments": comments,
                "comment_form": comment_form,
            })

    def post(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated comment submission: post_id=%s", pk)
            return redirect("login")

        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user

            parent_id = request.POST.get("parent_id")

            if parent_id:
                parent_comment = get_object_or_404(Comment, pk=parent_id)
                new_comment.parent = parent_comment

            new_comment.save()

            logger.info(
                "Comment created: comment_id=%s post_id=%s user_id=%s",
                new_comment.id,
                post.id,
                request.user.id,
            )

            return redirect("home")

        logger.warning(
            "Comment validation failed: post_id=%s user_id=%s",
            post.id,
            request.user.id,
        )

        return render(request,
            "comments.html",
            {
                "post": post,
                "comments": comments,
                "comment_form": comment_form,
            })


class DeleteCommentView(LoginRequiredMixin, View):
    """Delete a comment if the current user has permission."""
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)

        if (request.user == comment.author or request.user == comment.post.user):
            logger.info(
                "Comment deleted: comment_id=%s post_id=%s user_id=%s",
                comment.id,
                comment.post.id,
                request.user.id,
            )
            comment.delete()
        else:
            logger.warning(
                "Unauthorized comment deletion attempt: "
                "comment_id=%s post_id=%s user_id=%s",
                comment.id,
                comment.post.id,
                request.user.id,
            )

        return redirect(request.META.get("HTTP_REFERER", "home"))