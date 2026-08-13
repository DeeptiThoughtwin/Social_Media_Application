import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.Notifications.models import Notification


@pytest.mark.django_db
class TestNotificationViews:

    def test_notifications_view(self, client):
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

        client.login(
            username="alex",
            password="password123"
        )

        response = client.get(
            reverse("notifications")
        )

        assert response.status_code == 200
        assert notification in response.context["notifications"]

    def test_notifications_view_marks_unread_as_read(self, client):
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
            notification_type="like",
            is_read=False
        )

        client.login(
            username="alex",
            password="password123"
        )

        client.get(
            reverse("notifications")
        )

        notification.refresh_from_db()

        assert notification.is_read is True

    def test_notifications_view_only_shows_current_user_notifications(self, client):
        sender = User.objects.create_user(
            username="john",
            password="password123"
        )

        receiver = User.objects.create_user(
            username="alex",
            password="password123"
        )

        other_user = User.objects.create_user(
            username="sam",
            password="password123"
        )

        own_notification = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="like"
        )

        other_notification = Notification.objects.create(
            sender=sender,
            receiver=other_user,
            notification_type="follow"
        )

        client.login(
            username="alex",
            password="password123"
        )

        response = client.get(
            reverse("notifications")
        )

        notifications = response.context["notifications"]

        assert own_notification in notifications
        assert other_notification not in notifications

    def test_notification_count(self, client):
        sender = User.objects.create_user(
            username="john",
            password="password123"
        )

        receiver = User.objects.create_user(
            username="alex",
            password="password123"
        )

        Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="like",
            is_read=False
        )

        Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="follow",
            is_read=False
        )

        client.login(
            username="alex",
            password="password123"
        )

        response = client.get(
            reverse("notification_count")
        )

        assert response.status_code == 200
        assert response.json()["count"] == 2

    def test_notification_count_does_not_include_read_notifications(self, client):
        sender = User.objects.create_user(
            username="john",
            password="password123"
        )

        receiver = User.objects.create_user(
            username="alex",
            password="password123"
        )

        Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="like",
            is_read=False
        )

        Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="follow",
            is_read=True
        )

        client.login(
            username="alex",
            password="password123"
        )

        response = client.get(
            reverse("notification_count")
        )

        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_notification_count_for_no_notifications(self, client):
        user = User.objects.create_user(
            username="alex",
            password="password123"
        )

        client.login(
            username="alex",
            password="password123"
        )

        response = client.get(
            reverse("notification_count")
        )

        assert response.status_code == 200
        assert response.json()["count"] == 0
