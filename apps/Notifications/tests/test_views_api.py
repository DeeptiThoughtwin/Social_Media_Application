import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from apps.Notifications.models import Notification


@pytest.mark.django_db
class TestNotificationAPIView:

    def test_notification_list(self):
        client = APIClient()

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

        client.force_authenticate(user=receiver)

        response = client.get(
            "/Notifications/api/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_notification_list_marks_unread_as_read(self):
        client = APIClient()

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

        client.force_authenticate(user=receiver)

        response = client.get(
            "/Notifications/api/"
        )

        notification.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert notification.is_read is True

    def test_notification_list_only_shows_current_user(self):
        client = APIClient()

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

        Notification.objects.create(
            sender=sender,
            receiver=other_user,
            notification_type="follow"
        )

        client.force_authenticate(user=receiver)

        response = client.get(
            "/Notifications/api/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_notification_list_without_login(self):
        client = APIClient()

        response = client.get(
            "/Notifications/api/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_notification_count(self):
        client = APIClient()

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

        client.force_authenticate(user=receiver)

        response = client.get(
            "/Notifications/api/count/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["unread_count"] == 2

    def test_notification_count_does_not_include_read(self):
        client = APIClient()

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

        client.force_authenticate(user=receiver)

        response = client.get(
            "/Notifications/api/count/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["unread_count"] == 1

    def test_mark_notification_read(self):
        client = APIClient()

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

        client.force_authenticate(user=receiver)

        response = client.patch(
            f"/Notifications/api/{notification.id}/read/"
        )

        notification.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert notification.is_read is True
        assert response.data["message"] == "Notification marked as read"

    def test_user_cannot_mark_other_users_notification(self):
        client = APIClient()

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

        notification = Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="like",
            is_read=False
        )

        client.force_authenticate(user=other_user)

        response = client.patch(
            f"/Notifications/api/{notification.id}/read/"
        )

        notification.refresh_from_db()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert notification.is_read is False

    def test_mark_all_notifications_read(self):
        client = APIClient()

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

        client.force_authenticate(user=receiver)

        response = client.patch(
            "/Notifications/api/read-all/"
        )

        unread_count = Notification.objects.filter(
            receiver=receiver,
            is_read=False
        ).count()

        assert response.status_code == status.HTTP_200_OK
        assert unread_count == 0
        assert response.data["message"] == "All notifications marked as read"

    def test_mark_all_notifications_does_not_affect_other_user(self):
        client = APIClient()

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

        Notification.objects.create(
            sender=sender,
            receiver=receiver,
            notification_type="like",
            is_read=False
        )

        other_notification = Notification.objects.create(
            sender=sender,
            receiver=other_user,
            notification_type="like",
            is_read=False
        )

        client.force_authenticate(user=receiver)

        client.patch(
            "/Notifications/api/read-all/"
        )

        other_notification.refresh_from_db()

        assert other_notification.is_read is False
