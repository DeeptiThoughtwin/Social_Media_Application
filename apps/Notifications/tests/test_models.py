import pytest
from django.contrib.auth.models import User

from apps.Notifications.models import Notification
from apps.posts.models import Post


@pytest.mark.django_db
class TestNotificationModel:

    def test_create_notification(self):
        sender = User.objects.create_user(
            username="john",
            password="password123"
        )

        receiver = User.objects.create_user(
            username="alex",
            password="password123"
        )

        notification = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="like"
        )

        assert notification.sender == sender
        assert notification.receiver == receiver
        assert notification.notification_type == "like"
        assert notification.is_read is False

    def test_notification_with_post(self):
        sender = User.objects.create_user(
            username="john",
            password="password123"
        )

        receiver = User.objects.create_user(
            username="alex",
            password="password123"
        )

        post = Post.objects.create(
            user=receiver,
            caption="My post"
        )

        notification = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            post=post,
            notification_type="like"
        )

        assert notification.post == post
        assert notification.notification_type == "like"

    def test_notification_default_is_read(self):
        sender = User.objects.create_user(
            username="john",
            password="password123"
        )

        receiver = User.objects.create_user(
            username="alex",
            password="password123"
        )

        notification = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="follow"
        )

        assert notification.is_read is False

    def test_mark_notification_as_read(self):
        sender = User.objects.create_user(
            username="john",
            password="password123"
        )

        receiver = User.objects.create_user(
            username="alex",
            password="password123"
        )

        notification = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="like"
        )

        notification.is_read = True
        notification.save()

        notification.refresh_from_db()

        assert notification.is_read is True

    def test_notification_str(self):
        sender = User.objects.create_user(
            username="john",
            password="password123"
        )

        receiver = User.objects.create_user(
            username="alex",
            password="password123"
        )

        notification = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="like"
        )

        assert str(notification) == "john like alex"

    def test_notification_ordering(self):
        sender = User.objects.create_user(
            username="john",
            password="password123"
        )

        receiver = User.objects.create_user(
            username="alex",
            password="password123"
        )

        first = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="like"
        )

        second = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="follow"
        )

        notifications = Notification.objects.all()

        assert notifications.first() == second
        assert notifications.last() == first
