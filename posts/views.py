from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import Post, PostMedia, Like
from .forms import PostForm


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create_posts.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        files = self.request.FILES.getlist("files")
        for f in files:
            media_type = (
                "video" if f.content_type.startswith("video") else "image"
            )
            PostMedia.objects.create(
                post=post,
                file=f,
                media_type=media_type,
            )

        return redirect(self.success_url)


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("profile")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class LikePostView(LoginRequiredMixin, View):

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if created:
            liked = True
        else:
            like.delete()
            liked = False

        return JsonResponse({
            "liked": liked,
            "likes_count": post.likes.count()
        })


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"


class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/edit_post.html"
    success_url = reverse_lazy("profile")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user
