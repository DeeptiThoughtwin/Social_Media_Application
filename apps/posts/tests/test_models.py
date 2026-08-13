import pytest
from django.contrib.auth.models import User
from apps.posts.models import Post, PostMedia, Like


@pytest.mark.django_db
class TestPostModels:

    def test_create_post(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My first post"
        )

        assert post.user == user
        assert post.caption == "My first post"
        assert Post.objects.count() == 1

    def test_create_post_media(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My photo"
        )

        media = PostMedia.objects.create(
            post=post,
            file="posts/media/photo.jpg",
            media_type="image"
        )

        assert media.post == post
        assert media.media_type == "image"
        assert media.file.name == "posts/media/photo.jpg"

    def test_create_like(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        like = Like.objects.create(
            user=user,
            post=post
        )

        assert like.user == user
        assert like.post == post
        assert Like.objects.count() == 1

    def test_post_str(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="Hello world"
        )

        assert str(post) == "john - Hello world"

    def test_post_str_without_caption(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user
        )

        assert str(post) == "john - No Caption"

    def test_post_media_str(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        media = PostMedia.objects.create(
            post=post,
            file="posts/media/photo.jpg",
            media_type="image"
        )

        assert str(media) == "john - Image"

    def test_like_str(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        like = Like.objects.create(
            user=user,
            post=post
        )

        assert str(like) == f"john liked {post.id}"

    def test_user_can_like_post_only_once(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        Like.objects.create(
            user=user,
            post=post
        )

        with pytest.raises(Exception):
            Like.objects.create(
                user=user,
                post=post
            )
