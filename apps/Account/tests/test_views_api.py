import pytest
from unittest.mock import patch
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
from rest_framework import status
from apps.Account.models import Profile, Follow, PasswordResetOTP
from apps.posts.models import Post
from apps.Stories.models import Story
from apps.comments.models import Comment

@pytest.mark.django_db
class TestProfileAPIView:

    def test_get_profile(self):
        client = APIClient()
        user = User.objects.create_user(
            username="john",
            password="password123"
        )
        client.force_authenticate(user=user)
        response = client.get(
            "/api/profile/"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"] == user.id


    def test_profile_is_created_if_not_exists(self):
        client = APIClient()
        user = User.objects.create_user(
            username="john",
            password="password123"
        )
        Profile.objects.filter(user=user).delete()

        client.force_authenticate(user=user)
        assert Profile.objects.filter(
            user=user
        ).exists() is False

        response = client.get(
            "/api/profile/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert Profile.objects.filter(
            user=user
        ).exists() is True


    def test_profile_requires_login(self):
        client = APIClient()
        response = client.get(
            "/api/profile/"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED




@pytest.mark.django_db
class TestEditProfileAPIView:

    def test_edit_profile_success(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            email="old@gmail.com",
            password="password123"
        )

        client.force_authenticate(user=user)

        response = client.patch(
            "/api/profile/edit/",
            {
                "bio": "Backend Developer"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        profile = Profile.objects.get(
            user=user
        )

        assert profile.bio == "Backend Developer"


    def test_edit_profile_updates_user_data(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            email="old@gmail.com",
            password="password123"
        )

        client.force_authenticate(user=user)

        response = client.patch(
            "/api/profile/edit/",
            {
                "email": "new@gmail.com"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()

        assert user.email == "new@gmail.com"


    def test_edit_profile_requires_login(self):
        client = APIClient()

        response = client.patch(
            "/api/profile/edit/",
            {
                "bio": "Developer"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED





@pytest.mark.django_db
class TestDeleteProfileAPIView:

    def test_delete_profile_success(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.force_authenticate(user=user)

        response = client.delete(
            "/api/profile/delete/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert User.objects.filter(
            username="john"
        ).exists() is False


    def test_delete_profile_deletes_profile(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.force_authenticate(user=user)

        client.delete(
            "/api/profile/delete/"
        )

        assert Profile.objects.filter(
            user_id=user.id
        ).exists() is False


    def test_delete_profile_requires_login(self):
        client = APIClient()

        response = client.delete(
            "/api/profile/delete/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED



@pytest.mark.django_db
class TestFollowUserAPIView:

    def test_follow_user(self):
        client = APIClient()

        user1 = User.objects.create_user(
            username="john",
            password="password123"
        )

        user2 = User.objects.create_user(
            username="alex",
            password="password123"
        )

        client.force_authenticate(user=user1)

        response = client.post(
            f"/api/follow/{user2.id}/"
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data["following"] is True
        assert response.data["followers_count"] == 1

        assert Follow.objects.filter(
            follower=user1,
            following=user2
        ).exists()


    def test_unfollow_user(self):
        client = APIClient()

        user1 = User.objects.create_user(
            username="john",
            password="password123"
        )

        user2 = User.objects.create_user(
            username="alex",
            password="password123"
        )

        Follow.objects.create(
            follower=user1,
            following=user2
        )

        client.force_authenticate(user=user1)

        response = client.post(
            f"/api/follow/{user2.id}/"
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data["following"] is False

        assert Follow.objects.filter(
            follower=user1,
            following=user2
        ).exists() is False


    def test_cannot_follow_yourself(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.force_authenticate(user=user)

        response = client.post(
            f"/api/follow/{user.id}/"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert response.data["error"] == (
            "You cannot follow yourself."
        )


    def test_follow_requires_login(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        response = client.post(
            f"/api/follow/{user.id}/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED



@pytest.mark.django_db
class TestFeedAPIView:

    def test_get_feed(self):
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
            "/api/feed/"
        )

        assert response.status_code == status.HTTP_200_OK

        assert "posts" in response.data
        assert "stories" in response.data


    def test_feed_contains_posts(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        Post.objects.create(
            user=user,
            caption="Hello"
        )

        Post.objects.create(
            user=user,
            caption="Second post"
        )

        client.force_authenticate(user=user)

        response = client.get(
            "/api/feed/"
        )

        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["posts"]) == 2


    def test_feed_contains_stories(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = SimpleUploadedFile(
            "story.jpg",
            b"fake image",
            content_type="image/jpeg"
        )

        Story.objects.create(
            user=user,
            image=image
        )

        client.force_authenticate(user=user)

        response = client.get(
            "/api/feed/"
        )

        assert response.status_code == status.HTTP_200_OK

        assert len(response.data["stories"]) == 1


    def test_feed_requires_login(self):
        client = APIClient()

        response = client.get(
            "/api/feed/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED




@pytest.mark.django_db
class TestCommentAPIView:

    def test_get_comments(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        post = Post.objects.create(
            user=user,
            caption="My post"
        )

        Comment.objects.create(
            post=post,
            author=user,
            body="Nice post!"
        )

        client.force_authenticate(user=user)

        response = client.get(
            f"/api/posts/{post.id}/comments/"
        )

        assert response.status_code == status.HTTP_200_OK

        assert len(response.data) == 1


    def test_create_comment(self):
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
            f"/api/posts/{post.id}/comments/",
            {
                "body": "Nice post!"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert Comment.objects.count() == 1

        comment = Comment.objects.first()

        assert comment.post == post
        assert comment.author == user
        assert comment.body == "Nice post!"


    def test_comment_requires_login(self):
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
            f"/api/posts/{post.id}/comments/",
            {
                "body": "Nice post!"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        assert Comment.objects.count() == 0




@pytest.mark.django_db
class TestForgotPasswordAPIView:
    def test_forgot_password_success(self, monkeypatch):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="password123"
        )

        def fake_send_mail(*args, **kwargs):
            return True

        monkeypatch.setattr(
            "apps.Account.api.views.send_mail",
            fake_send_mail
        )

        response = client.post(
            "/api/forgot-password/",
            {
                "email": "john@gmail.com"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data["message"] == (
            "OTP sent successfully."
        )

        assert PasswordResetOTP.objects.filter(
            user=user
        ).exists()


    def test_forgot_password_user_not_found(self, monkeypatch):
        client = APIClient()

        def fake_send_mail(*args, **kwargs):
            return True

        monkeypatch.setattr(
            "apps.Account.api.views.send_mail",
            fake_send_mail
        )

        response = client.post(
            "/api/forgot-password/",
            {
                "email": "unknown@gmail.com"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert response.data["error"] == (
            "User with this email does not exist."
        )


    def test_forgot_password_without_email(self):
        client = APIClient()

        response = client.post(
            "/api/forgot-password/",
            {},
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST



@pytest.mark.django_db
class TestVerifyOTPAPIView:

    def test_verify_otp_invalid(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="password123"
        )

        PasswordResetOTP.objects.create(
            user=user,
            otp="123456"
        )

        session = client.session
        session["reset_user"] = user.id
        session.save()

        response = client.post(
            "/api/verify-otp/",
            {
                "otp": "999999",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "OTP is incorrect or expired."

    def test_verify_otp_requires_password_reset_request(self):
        client = APIClient()

        response = client.post(
            "/api/verify-otp/",
            {
                "otp": "123456",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Please request password reset first."

    def test_verify_otp_success(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="password123",
        )

        PasswordResetOTP.objects.create(
            user=user,
            otp="123456"
        )

        session = client.session
        session["reset_user"] = user.id
        session.save()

        with patch(
            "rest_framework.throttling.SimpleRateThrottle.allow_request",
            return_value=True
        ):
            response = client.post(
                "/api/verify-otp/",
                {
                    "otp": "123456",
                },
                format="json"
            )

        assert response.status_code == status.HTTP_200_OK

    def test_verify_otp_missing_otp(self):
        client = APIClient()
        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="password123",
        )

        session = client.session
        session["reset_user"] = user.id
        session.save()

        response = client.post(
            "/api/verify-otp/",
            {},
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        

    def test_verify_otp_missing_otp(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="password123",
        )

        session = client.session
        session["reset_user"] = user.id
        session.save()

        with patch(
            "rest_framework.throttling.SimpleRateThrottle.allow_request",
            return_value=True
        ):
            response = client.post(
                "/api/verify-otp/",
                {},
                format="json"
            )

        assert response.status_code == status.HTTP_400_BAD_REQUEST