import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.posts.models import Post
from apps.comments.models import Comment


@pytest.mark.django_db
class TestCommentViews:

    def test_comment_view_get(self, client):
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
            reverse("comment_view", kwargs={"pk": post.id})
        )

        assert response.status_code == 200
        assert response.context["post"] == post
        assert "comments" in response.context
        assert "comment_form" in response.context

    def test_create_comment(self, client):
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
            reverse("comment_view", kwargs={"pk": post.id}),
            {
                "body": "Nice post!"
            }
        )

        assert response.status_code == 302
        assert response.url == reverse("home")

        assert Comment.objects.count() == 1

        comment = Comment.objects.first()

        assert comment.post == post
        assert comment.author == user
        assert comment.body == "Nice post!"

    def test_create_reply(self, client):
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

        client.login(
            username="john",
            password="password123"
        )

        response = client.post(
            reverse("comment_view", kwargs={"pk": post.id}),
            {
                "body": "This is a reply",
                "parent_id": parent_comment.id
            }
        )

        assert response.status_code == 302

        reply = Comment.objects.get(
            body="This is a reply"
        )

        assert reply.parent == parent_comment
        assert reply.post == post
        assert reply.author == user

    def test_comment_view_shows_only_active_comments(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        active_comment = Comment.objects.create(
            post=post,
            author=user,
            body="Active comment",
            active=True
        )

        inactive_comment = Comment.objects.create(
            post=post,
            author=user,
            body="Inactive comment",
            active=False
        )

        client.login(
            username="john",
            password="password123"
        )

        response = client.get(
            reverse("comment_view", kwargs={"pk": post.id})
        )

        comments = response.context["comments"]

        assert active_comment in comments
        assert inactive_comment not in comments

    def test_unauthenticated_user_cannot_create_comment(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        response = client.post(
            reverse("comment_view", kwargs={"pk": post.id}),
            {
                "body": "Nice post!"
            }
        )

        assert response.status_code == 302
        assert response.url == reverse("login")
        assert Comment.objects.count() == 0

    def test_delete_comment_by_author(self, client):
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

        client.login(
            username="john",
            password="password123"
        )

        response = client.post(
            reverse("delete_comment", kwargs={"pk": comment.id}),
            HTTP_REFERER=reverse("home")
        )

        assert response.status_code == 302
        assert Comment.objects.count() == 0

    def test_post_owner_can_delete_comment(self, client):
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

        client.login(
            username="john",
            password="password123"
        )

        response = client.post(
            reverse("delete_comment", kwargs={"pk": comment.id}),
            HTTP_REFERER=reverse("home")
        )

        assert response.status_code == 302
        assert Comment.objects.count() == 0

    def test_other_user_cannot_delete_comment(self, client):
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

        client.login(
            username="sam",
            password="password123"
        )

        response = client.post(
            reverse("delete_comment", kwargs={"pk": comment.id}),
            HTTP_REFERER=reverse("home")
        )

        assert response.status_code == 302
        assert Comment.objects.count() == 1
