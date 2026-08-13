import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.posts.models import Post, PostMedia, Like
from django.contrib import messages


@pytest.mark.django_db
class TestPostViews:

    def test_create_post_success(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.login(
            username="john",
            password="password123"
        )

        image = SimpleUploadedFile(
            "photo.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )

        response = client.post(
            reverse("create_post"),
            {
                "caption": "My first post",
                "files": image,
            }
        )

        assert response.status_code == 302
        assert Post.objects.count() == 1
        assert PostMedia.objects.count() == 1

        post = Post.objects.first()

        assert post.user == user
        assert post.caption == "My first post"

    def test_create_post_without_file(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.login(
            username="john",
            password="password123"
        )

        response = client.post(
            reverse("create_post"),
            {
                "caption": "Post without image",
            }
        )

        assert response.status_code == 200
        assert Post.objects.count() == 0
        assert PostMedia.objects.count() == 0

    def test_create_post_rejects_invalid_file(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.login(
            username="john",
            password="password123"
        )

        file = SimpleUploadedFile(
            "file.svg",
            b"fake svg content",
            content_type="image/svg+xml"
        )

        response = client.post(
            reverse("create_post"),
            {
                "caption": "Invalid file",
                "files": file,
            }
        )

        assert response.status_code == 200
        assert Post.objects.count() == 0
        assert PostMedia.objects.count() == 0

    def test_delete_post_by_owner(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        client.login(
            username="john",
            password="password123"
        )

        response = client.post(
            reverse("delete_post", kwargs={"pk": post.id})
        )

        assert response.status_code == 302
        assert Post.objects.count() == 0

    def test_delete_post_by_other_user_is_forbidden(self, client):
        owner = User.objects.create_user(
            username="john",
            password="password123"
        )

        other_user = User.objects.create_user(
            username="alex",
            password="password123"
        )

        post = Post.objects.create(
            user=owner,
            caption="John's post"
        )

        client.login(
            username="alex",
            password="password123"
        )

        response = client.post(
            reverse("delete_post", kwargs={"pk": post.id})
        )

        assert response.status_code == 403
        assert Post.objects.count() == 1

    def test_like_post(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        client.login(
            username="john",
            password="password123"
        )

        response = client.post(
            reverse("like_post", kwargs={"post_id": post.id})
        )

        assert response.status_code == 200
        assert response.json()["liked"] is True
        assert response.json()["likes_count"] == 1
        assert Like.objects.count() == 1

    def test_unlike_post(self, client):
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

        client.login(
            username="john",
            password="password123"
        )

        response = client.post(
            reverse("like_post", kwargs={"post_id": post.id})
        )

        assert response.status_code == 200
        assert response.json()["liked"] is False
        assert response.json()["likes_count"] == 0
        assert Like.objects.count() == 0

    def test_post_detail(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        client.login(
            username="john",
            password="password123"
        )

        response = client.get(
            reverse("post_detail", kwargs={"post_id": post.id})
        )

        assert response.status_code == 200
        assert response.context["post"] == post

    def test_edit_post_by_owner(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="Old caption"
        )

        client.login(
            username="john",
            password="password123"
        )

        response = client.post(
            reverse("edit_post", kwargs={"pk": post.id}),
            {
                "caption": "New caption",
            }
        )

        assert response.status_code == 302

        post.refresh_from_db()

        assert post.caption == "New caption"

    def test_edit_post_by_other_user_is_forbidden(self, client):
        owner = User.objects.create_user(
            username="john",
            password="password123"
        )

        other_user = User.objects.create_user(
            username="alex",
            password="password123"
        )

        post = Post.objects.create(
            user=owner,
            caption="John's post"
        )

        client.login(
            username="alex",
            password="password123"
        )

        response = client.post(
            reverse("edit_post", kwargs={"pk": post.id}),
            {
                "caption": "Changed caption",
            }
        )

        assert response.status_code == 403

        post.refresh_from_db()

        assert post.caption == "John's post"
