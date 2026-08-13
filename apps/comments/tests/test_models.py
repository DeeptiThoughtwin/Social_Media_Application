import pytest
from django.contrib.auth.models import User

from apps.comments.models import Comment
from apps.posts.models import Post


@pytest.mark.django_db
class TestCommentModel:

    def test_create_comment(self):
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
            body="Nice post!"
        )

        assert comment.post == post
        assert comment.author == user
        assert comment.body == "Nice post!"
        assert comment.active is True

    def test_comment_str(self):
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
            body="Nice post!"
        )

        assert str(comment) == "Comment by john"

    def test_comment_default_active(self):
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
            body="Hello"
        )

        assert comment.active is True

    def test_reply_to_comment(self):
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
            body="First comment"
        )

        reply = Comment.objects.create(
            post=post,
            author=user,
            body="This is a reply",
            parent=comment
        )

        assert reply.parent == comment
        assert reply in comment.replies.all()

    def test_comment_can_have_multiple_replies(self):
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
            body="First comment"
        )

        reply1 = Comment.objects.create(
            post=post,
            author=user,
            body="First reply",
            parent=comment
        )

        reply2 = Comment.objects.create(
            post=post,
            author=user,
            body="Second reply",
            parent=comment
        )

        assert comment.replies.count() == 2
        assert reply1 in comment.replies.all()
        assert reply2 in comment.replies.all()

    def test_comment_ordering(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        comment1 = Comment.objects.create(
            post=post,
            author=user,
            body="First comment"
        )

        comment2 = Comment.objects.create(
            post=post,
            author=user,
            body="Second comment"
        )

        comments = Comment.objects.all()

        assert comments.first() == comment1
        assert comments.last() == comment2
