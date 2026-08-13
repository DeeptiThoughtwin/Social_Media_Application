
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.posts.models import Post, Like


@pytest.mark.django_db
class TestPostViewSet:

    def test_list_posts(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        Post.objects.create(
            user=user,
            caption="My post"
        )

        client.force_authenticate(user=user)

        response = client.get(
            "/posts/api/posts/"
        )

        assert response.status_code == status.HTTP_200_OK

    def test_create_post(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.force_authenticate(user=user)

        response = client.post(
            "/posts/api/posts/",
            {
                "caption": "My new post"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1

        post = Post.objects.first()

        assert post.user == user
        assert post.caption == "My new post"

    def test_create_post_without_login(self):
        client = APIClient()

        response = client.post(
            "/posts/api/posts/",
            {
                "caption": "My post"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Post.objects.count() == 0

    def test_update_own_post(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="Old caption"
        )

        client.force_authenticate(user=user)

        response = client.patch(
            f"/posts/api/posts/{post.id}/",
            {
                "caption": "New caption"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        post.refresh_from_db()

        assert post.caption == "New caption"

    def test_other_user_cannot_update_post(self):
        client = APIClient()

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
            caption="Original"
        )

        client.force_authenticate(user=other_user)

        response = client.patch(
            f"/posts/api/posts/{post.id}/",
            {
                "caption": "Changed"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        post.refresh_from_db()

        assert post.caption == "Original"

    def test_delete_own_post(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="Delete me"
        )

        client.force_authenticate(user=user)

        response = client.delete(
            f"/posts/api/posts/{post.id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Post.objects.count() == 0

    def test_other_user_cannot_delete_post(self):
        client = APIClient()

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
            caption="My post"
        )

        client.force_authenticate(user=other_user)

        response = client.delete(
            f"/posts/api/posts/{post.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Post.objects.count() == 1

    def test_like_post(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        client.force_authenticate(user=user)

        response = client.post(
            f"/posts/api/posts/{post.id}/like/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["liked"] is True
        assert response.data["likes_count"] == 1
        assert Like.objects.count() == 1

    def test_unlike_post(self):
        client = APIClient()

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

        client.force_authenticate(user=user)

        response = client.post(
            f"/posts/api/posts/{post.id}/like/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["liked"] is False
        assert response.data["likes_count"] == 0
        assert Like.objects.count() == 0


@pytest.mark.django_db
class TestLikeViewSet:

    def test_create_like(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        client.force_authenticate(user=user)

        response = client.post(
            "/posts/api/likes/",
            {
                "post": post.id
            },
            format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Like.objects.count() == 1

        like = Like.objects.first()

        assert like.user == user
        assert like.post == post

    def test_create_like_without_login(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        response = client.post(
            "/posts/api/likes/",
            {
                "post": post.id
            },
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Like.objects.count() == 0
