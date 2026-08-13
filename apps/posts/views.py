import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from apps.posts.models import Post, PostMedia, Like
from apps.posts.forms import PostForm
from django.http import HttpResponse
from django.db import transaction


logger = logging.getLogger(__name__)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create_posts.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        files = self.request.FILES.getlist("files")

        if not files:
            logger.warning(
                "Post creation failed: no media uploaded, user_id=%s",
                self.request.user.id,
            )

            form.add_error(
                None,
                "Please upload at least one image or video."
            )
            return self.form_invalid(form)

        ALLOWED_IMAGE_TYPES = [
            "image/jpeg",
            "image/png",
        ]

        ALLOWED_VIDEO_TYPES = [
            "video/mp4",
            "video/webm",
        ]

        for f in files:
            if (
                f.content_type not in ALLOWED_IMAGE_TYPES
                and f.content_type not in ALLOWED_VIDEO_TYPES
            ):
                logger.warning(
                    "Post creation failed: unsupported file type "
                    "user_id=%s file=%s content_type=%s",
                    self.request.user.id,
                    f.name,
                    f.content_type,
                )

                form.add_error(
                    None,
                    f"{f.name} is not a supported file type."
                )
                return self.form_invalid(form)

        with transaction.atomic():
            post = form.save(commit=False)
            post.user = self.request.user
            post.save()

            for f in files:
                media_type = (
                    "video"
                    if f.content_type in ALLOWED_VIDEO_TYPES
                    else "image"
                )

                PostMedia.objects.create(
                    post=post,
                    file=f,
                    media_type=media_type,
                )

        logger.info(
            "Post created successfully: post_id=%s user_id=%s media_count=%s",
            post.id,
            self.request.user.id,
            len(files),
        )

        return super().form_valid(form)


class DeletePostView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Post
    success_url = reverse_lazy("profile")

    def test_func(self):
        post = self.get_object()

        is_owner = self.request.user == post.user

        if is_owner:
            logger.info(
                "Post deletion authorized: post_id=%s user_id=%s",
                post.id,
                self.request.user.id,
            )
        else:
            logger.warning(
                "Unauthorized post deletion attempt: "
                "post_id=%s user_id=%s owner_id=%s",
                post.id,
                self.request.user.id,
                post.user.id,
            )

        return is_owner


class LikePostView(LoginRequiredMixin, View):

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if created:
            liked = True

            logger.info(
                "Post liked: post_id=%s user_id=%s",
                post.id,
                request.user.id,
            )

        else:
            like.delete()
            liked = False

            logger.info(
                "Post unliked: post_id=%s user_id=%s",
                post.id,
                request.user.id,
            )

        likes_count = post.likes.count()

        return JsonResponse({
            "liked": liked,
            "likes_count": likes_count
        })


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def get(self, request, *args, **kwargs):
        logger.info(
            "Post detail viewed: post_id=%s user_id=%s",
            kwargs.get(self.pk_url_kwarg),
            request.user.id,
        )

        return super().get(request, *args, **kwargs)


class EditPostView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Post
    form_class = PostForm
    template_name = "posts/edit_post.html"
    success_url = reverse_lazy("profile")

    def test_func(self):
        post = self.get_object()

        is_owner = self.request.user == post.user

        if is_owner:
            logger.info(
                "Post edit authorized: post_id=%s user_id=%s",
                post.id,
                self.request.user.id,
            )
        else:
            logger.warning(
                "Unauthorized post edit attempt: "
                "post_id=%s user_id=%s owner_id=%s",
                post.id,
                self.request.user.id,
                post.user.id,
            )

        return is_owner



def test_sentry(request):
    number = 10 / 0

    return HttpResponse("Sentry is working!")
    
