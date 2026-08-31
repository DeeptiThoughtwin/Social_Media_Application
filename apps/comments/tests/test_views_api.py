import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from apps.posts.models import Post
from apps.comments.models import Comment


@pytest.mark.django_db
class TestCommentAPIView:

    # def test_get_comments(self):
    #     client = APIClient()

    #     user = User.objects.create_user(
    #         username="john",
    #         password="password123"
    #     )

    #     post = Post.objects.create(
    #         user=user,
    #         caption="My post"
    #     )

    #     comment = Comment.objects.create(
    #         post=post,
    #         author=user,
    #         body="Nice post!"
    #     )

    #     response = client.get(
    #         f"/comments/api/posts/{post.id}/comments/"
    #     )

        # assert response.status_code == status.HTTP_200_OK
        # assert len(response.data) == 1
        # assert response.data[0]["body"] == "Nice post"

    # def test_get_comments_only_active(self):
    #     client = APIClient()

    #     user = User.objects.create_user(
    #         username="john",
    #         password="password123"
    #     )

    #     post = Post.objects.create(
    #         user=user,
    #         caption="My post"
    #     )

    #     Comment.objects.create(
    #         post=post,
    #         author=user,
    #         body="Active comment",
    #         active=True
    #     )

    #     Comment.objects.create(
    #         post=post,
    #         author=user,
    #         body="Inactive comment",
    #         active=False
    #     )

    #     response = client.get(
    #         f"/comments/api/posts/{post.id}/comments/"
    #     )

    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 1
    #     assert response.data[0]["body"] == "Active comment"

    def test_create_comment_authenticated_user(self):
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
            f"/comments/api/posts/{post.id}/comments/",
            {
                "body": "My comment"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == 1

        comment = Comment.objects.first()

        assert comment.author == user
        assert comment.post == post
        assert comment.body == "My comment"

    def test_create_comment_without_login(self):
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
            f"/comments/api/posts/{post.id}/comments/",
            {
                "body": "My comment"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Comment.objects.count() == 0

    def test_create_reply(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        parent_comment = Comment.objects.create(
            post=post,
            author=user,
            body="First comment"
        )

        client.force_authenticate(user=user)

        response = client.post(
            f"/comments/api/posts/{post.id}/comments/",
            {
                "body": "This is a reply",
                "parent": parent_comment.id
            },
            format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED

        reply = Comment.objects.get(
            body="This is a reply"
        )

        assert reply.parent == parent_comment
        assert reply.author == user
        assert reply.post == post

    def test_delete_comment_by_author(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        comment = Comment.objects.create(
            post=post,
            author=user,
            body="Delete me"
        )

        client.force_authenticate(user=user)

        response = client.delete(
            f"/comments/api/comments/{comment.id}/delete/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Comment.objects.count() == 0

    def test_post_owner_can_delete_comment(self):
        client = APIClient()

        owner = User.objects.create_user(
            username="john",
            password="password123"
        )

        commenter = User.objects.create_user(
            username="alex",
            password="password123"
        )

        post = Post.objects.create(
            user=owner,
            caption="My post"
        )

        comment = Comment.objects.create(
            post=post,
            author=commenter,
            body="Comment"
        )

        client.force_authenticate(user=owner)

        response = client.delete(
            f"/comments/api/comments/{comment.id}/delete/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Comment.objects.count() == 0

    def test_other_user_cannot_delete_comment(self):
        client = APIClient()

        owner = User.objects.create_user(
            username="john",
            password="password123"
        )

        commenter = User.objects.create_user(
            username="alex",
            password="password123"
        )

        other_user = User.objects.create_user(
            username="sam",
            password="password123"
        )

        post = Post.objects.create(
            user=owner,
            caption="My post"
        )

        comment = Comment.objects.create(
            post=post,
            author=commenter,
            body="Comment"
        )

        client.force_authenticate(user=other_user)

        response = client.delete(
            f"/comments/api/comments/{comment.id}/delete/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Comment.objects.count() == 1
