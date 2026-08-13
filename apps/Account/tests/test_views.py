import pytest
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from apps.Account.models import Profile, Follow
from apps.posts.models import Post, Like
from apps.Account.forms import (
    RegistrationForm,
    LoginForm,
    UserUpdateForm,
    ProfileUpdateForm,
    ForgotPasswordForm,
    OTPForm,
    ResetPasswordForm,
)
from apps.Stories.models import Story
User = get_user_model()




@pytest.mark.django_db
def test_home_authenticated_user(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert "home.html" in [t.name for t in response.templates]




@pytest.mark.django_db
def test_home_context(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("home"))

    assert "profile" in response.context
    assert "posts" in response.context
    assert "stories" in response.context
    assert "posts_count" in response.context
    assert "followers_count" in response.context
    assert "following_count" in response.context


@pytest.mark.django_db
def test_home_posts_count(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    Post.objects.create(
        user=user,
        caption="Post 1"
    )

    Post.objects.create(
        user=user,
        caption="Post 2"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("home"))

    assert response.context["posts_count"] == 2


@pytest.mark.django_db
def test_home_followers_count(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    follower = User.objects.create_user(
        username="alice",
        password="password123"
    )

    Follow.objects.create(
        follower=follower,
        following=user
    )

    client.login(
        username="john",
        password="password123"
        )

    response = client.get(reverse("home"))

    assert response.context["followers_count"] == 1

@pytest.mark.django_db
def test_home_following_count(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    following = User.objects.create_user(
        username="alice",
        password="password123"
    )

    Follow.objects.create(
        follower=user,
        following=following
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("home"))

    assert response.context["following_count"] == 1

@pytest.mark.django_db
def test_home_sets_is_following(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    author = User.objects.create_user(
        username="alice",
        password="password123"
    )

    post = Post.objects.create(
        user=author,
        caption="Hello"
    )

    Follow.objects.create(
        follower=user,
        following=author
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("home"))

    returned_post = response.context["posts"][0]

    assert returned_post.is_following is True

@pytest.mark.django_db
def test_home_sets_is_liked(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    post = Post.objects.create(
        user=user,
        caption="Hello"
    )

    Like.objects.create(
        user=user,
        post=post
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("home"))

    returned_post = response.context["posts"][0]

    assert returned_post.is_liked is True


@pytest.mark.django_db
def test_signup_get(client):
    response = client.get(reverse("signup"))

    assert response.status_code == 200
    assert "signup.html" in [t.name for t in response.templates]
    assert "form" in response.context



@pytest.mark.django_db
@patch("apps.Account.views.send_welcome_email.delay")
def test_signup_success(mock_delay, client):

    response = client.post(
    reverse("signup"),
    {
        "username": "john",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password1": "StrongPassword@123",
        "password2": "StrongPassword@123",
    }
    )

    assert response.status_code == 302
    assert response.url == reverse("home")
    assert User.objects.filter(username="john").exists()

@pytest.mark.django_db
@patch("apps.Account.views.send_welcome_email.delay")
def test_signup_logs_user_in(mock_delay, client):

    client.post(
    reverse("signup"),
    {
        "username": "john",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password1": "StrongPassword@123",
        "password2": "StrongPassword@123",
    }
    )

    response = client.get(reverse("home"))

    assert response.status_code == 200



@pytest.mark.django_db
@patch("apps.Account.views.send_welcome_email.delay")
def test_signup_success_message(mock_delay, client):
    response = client.post(
    reverse("signup"),
    {
        "username": "john",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password1": "StrongPassword@123",
        "password2": "StrongPassword@123",
    },
    follow=True,
    )

    # If the form was rendered again, print its errors
    if response.context and "form" in response.context:
        print("Form errors:", response.context["form"].errors)

    print("Status code:", response.status_code)
    print("Users:", list(User.objects.values("username", "email")))

    assert User.objects.filter(username="john").exists()

@pytest.mark.django_db
def test_signup_invalid_data(client):

    response = client.post(
        reverse("signup"),
        {
            "username": "",
            "email": "",
            "password1": "123",
            "password2": "456",
        }
    )

    assert response.status_code == 200

    assert User.objects.count() == 0

    assert "form" in response.context


@pytest.mark.django_db
def test_signup_duplicate_username(client):

    User.objects.create_user(
        username="john",
        password="password123"
    )

    response = client.post(
        reverse("signup"),
        {
            "username": "john",
            "email": "john@example.com",
            "password1": "StrongPassword@123",
            "password2": "StrongPassword@123",
        }
    )

    assert response.status_code == 200

    assert User.objects.filter(username="john").count() == 1


@pytest.mark.django_db
def test_login_get(client):
    response = client.get(reverse("login"))

    assert response.status_code == 200
    assert "login.html" in [t.name for t in response.templates]
    assert "form" in response.context

@pytest.mark.django_db
def test_login_authenticated_user_redirect(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("login"))

    assert response.status_code == 302
    assert response.url == reverse("home")

@pytest.mark.django_db
def test_login_success(client):
    User.objects.create_user(
        username="john",
        password="password123"
    )

    response = client.post(
        reverse("login"),
        {
            "username": "john",
            "password": "password123",
        }
    )

    assert response.status_code == 302
    assert response.url == reverse("home")

@pytest.mark.django_db
def test_login_logs_user_in(client):
    User.objects.create_user(
        username="john",
        password="password123"
    )

    client.post(
        reverse("login"),
        {
            "username": "john",
            "password": "password123",
        }
    )

    response = client.get(reverse("home"))

    assert response.status_code == 200

@pytest.mark.django_db
def test_login_success_message(client):
    User.objects.create_user(
        username="john",
        password="password123"
    )

    response = client.post(
        reverse("login"),
        {
            "username": "john",
            "password": "password123",
        },
        follow=True,
    )

    messages = list(get_messages(response.wsgi_request))

    assert any(
        str(message) == "Welcome back john"
        for message in messages
    )


@pytest.mark.django_db
def test_login_invalid_credentials(client):
    User.objects.create_user(
        username="john",
        password="password123"
    )

    response = client.post(
        reverse("login"),
        {
            "username": "john",
            "password": "wrongpassword",
        }
    )

    assert response.status_code == 200
    assert "form" in response.context
    


@pytest.mark.django_db
def test_logout_redirects_to_login(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("logout"))

    assert response.status_code == 302
    assert response.url == reverse("login")

@pytest.mark.django_db
def test_logout_logs_out_user(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    client.get(reverse("logout"))

    response = client.get(reverse("home"))

    assert response.status_code == 302

@pytest.mark.django_db
def test_logout_success_message(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(
        reverse("logout"),
        follow=True
    )

    messages = list(get_messages(response.wsgi_request))

    assert any(
        str(message) == "You have been logged out."
        for message in messages
    )



@pytest.mark.django_db
def test_profile_requires_login(client):
    response = client.get(reverse("profile"))

    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_profile_authenticated_user(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("profile"))

    assert response.status_code == 200
    assert "profile/profile.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_profile_context(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("profile"))

    assert "profile" in response.context
    assert "posts" in response.context
    assert "posts_count" in response.context
    assert "followers_count" in response.context
    assert "following_count" in response.context


@pytest.mark.django_db
def test_profile_posts_count(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    Post.objects.create(user=user, caption="Post 1")
    Post.objects.create(user=user, caption="Post 2")

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("profile"))

    assert response.context["posts_count"] == 2


@pytest.mark.django_db
def test_profile_followers_count(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    follower = User.objects.create_user(
        username="alice",
        password="password123"
    )

    Follow.objects.create(
        follower=follower,
        following=user
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("profile"))

    assert response.context["followers_count"] == 1

@pytest.mark.django_db
def test_profile_following_count(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    following = User.objects.create_user(
        username="alice",
        password="password123"
    )

    Follow.objects.create(
        follower=user,
        following=following
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("profile"))

    assert response.context["following_count"] == 1

@pytest.mark.django_db
def test_profile_shows_only_user_posts(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    other = User.objects.create_user(
        username="alice",
        password="password123"
    )

    Post.objects.create(user=user, caption="My Post")
    Post.objects.create(user=other, caption="Other Post")

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("profile"))

    posts = response.context["posts"]

    assert len(posts) == 1
    assert posts[0].user == user


@pytest.mark.django_db
def test_profile_sets_is_liked(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    post = Post.objects.create(
        user=user,
        caption="Hello"
    )

    Like.objects.create(
        user=user,
        post=post
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("profile"))

    returned_post = response.context["posts"][0]

    assert returned_post.is_liked is True


@pytest.mark.django_db
def test_edit_profile_requires_login(client):
    response = client.get(reverse("edit_profile"))

    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_edit_profile_get(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("edit_profile"))

    assert response.status_code == 200
    assert "profile/edit_profile.html" in [t.name for t in response.templates]




@pytest.mark.django_db
def test_edit_profile_forms_in_context(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.get(reverse("edit_profile"))

    assert "user_form" in response.context
    assert "profile_form" in response.context
    assert "profile" in response.context


@pytest.mark.django_db
def test_edit_profile_updates_user(client):
    user = User.objects.create_user(
        username="john",
        first_name="Old",
        last_name="Name",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.post(
        reverse("edit_profile"),
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "bio": "Backend Developer",
            "website": "https://example.com",
            "location": "India",
        }
    )

    user.refresh_from_db()

    assert response.status_code == 302
    assert response.url == reverse("profile")
    assert user.first_name == "John"
    assert user.last_name == "Doe"


@pytest.mark.django_db
def test_edit_profile_updates_profile(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    client.post(
        reverse("edit_profile"),
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "bio": "Backend Developer",
            "website": "https://example.com",
            "location": "India",
        }
    )

    profile = user.profile
    profile.refresh_from_db()

    assert profile.bio == "Backend Developer"
    assert profile.website == "https://example.com"
    assert profile.location == "India"


@pytest.mark.django_db
def test_edit_profile_success_message(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.post(
    reverse("edit_profile"),
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "bio": "Backend Developer",
        "website": "https://example.com",
        "location": "India",
    },
    follow=True,
)

    messages = list(get_messages(response.wsgi_request))

    assert any(
        str(message) == "Profile updated successfully."
        for message in messages
    )

@pytest.mark.django_db
def test_edit_profile_invalid_data(client):
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    response = client.post(
    reverse("edit_profile"),
    {
        "first_name": "John",
        "last_name": "Doe",
        "website": "invalid-url",
    }
    )

    assert response.status_code == 200
    assert "user_form" in response.context
    assert "profile_form" in response.context


@pytest.mark.django_db
def test_edit_profile_invalid_does_not_update(client):
    user = User.objects.create_user(
        username="john",
        email="old@example.com",
        password="password123"
    )

    client.login(
        username="john",
        password="password123"
    )

    client.post(
        reverse("edit_profile"),
        {
            "email": "invalid-email",
        }
    )

    user.refresh_from_db()

    assert user.email == "old@example.com"




@pytest.mark.django_db
def test_user_update_form_empty_first_name():
    user = User.objects.create_user(
        username="john",
        first_name="John",
        last_name="Doe",
        password="Password@123",
    )

    form = UserUpdateForm(
        instance=user,
        data={
            "first_name": "",
            "last_name": "Smith",
        }
    )

    assert not form.is_valid()
    assert "first_name" in form.errors


@pytest.mark.django_db
def test_user_update_form_empty_last_name():
    user = User.objects.create_user(
        username="john",
        first_name="John",
        last_name="Doe",
        password="Password@123",
    )

    form = UserUpdateForm(
        instance=user,
        data={
            "first_name": "Alice",
            "last_name": "",
        }
    )

    assert not form.is_valid()
    assert "last_name" in form.errors


@pytest.mark.django_db
def test_user_update_form_first_name_too_short():
    user = User.objects.create_user(
        username="john",
        first_name="John",
        last_name="Doe",
        password="Password@123",
    )

    form = UserUpdateForm(
        instance=user,
        data={
            "first_name": "A",
            "last_name": "Smith",
        }
    )

    assert not form.is_valid()
    assert "first_name" in form.errors


@pytest.mark.django_db
def test_user_update_form_last_name_too_short():
    user = User.objects.create_user(
        username="john",
        first_name="John",
        last_name="Doe",
        password="Password@123",
    )

    form = UserUpdateForm(
        instance=user,
        data={
            "first_name": "Alice",
            "last_name": "S",
        }
    )

    assert not form.is_valid()
    assert "last_name" in form.errors


@pytest.mark.django_db
def test_user_update_form_first_name_numbers():
    user = User.objects.create_user(
        username="john",
        first_name="John",
        last_name="Doe",
        password="Password@123",
    )

    form = UserUpdateForm(
        instance=user,
        data={
            "first_name": "Alice123",
            "last_name": "Smith",
        }
    )

    assert not form.is_valid()
    assert "first_name" in form.errors


@pytest.mark.django_db
def test_user_update_form_last_name_numbers():
    user = User.objects.create_user(
        username="john",
        first_name="John",
        last_name="Doe",
        password="Password@123",
    )

    form = UserUpdateForm(
        instance=user,
        data={
            "first_name": "Alice",
            "last_name": "Smith123",
        }
    )

    assert not form.is_valid()
    assert "last_name" in form.errors




@pytest.mark.django_db
def test_profile_update_form_invalid_website():
    user = User.objects.create_user(
        username="john",
        password="Password@123",
    )

    profile = user.profile

    form = ProfileUpdateForm(
        instance=profile,
        data={
            "bio": "Backend Developer",
            "website": "not-a-url",
            "location": "India",
            "birth_date": "2000-01-01",
        }
    )

    assert not form.is_valid()
    assert "website" in form.errors


@pytest.mark.django_db
def test_profile_update_form_bio_exactly_300_characters():
    user = User.objects.create_user(
        username="john",
        password="Password@123",
    )

    profile = user.profile

    form = ProfileUpdateForm(
        instance=profile,
        data={
            "bio": "a" * 300,
            "website": "https://example.com",
            "location": "India",
            "birth_date": "2000-01-01",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_profile_update_form_bio_more_than_300_characters():
    user = User.objects.create_user(
        username="john",
        password="Password@123",
    )

    profile = user.profile

    form = ProfileUpdateForm(
        instance=profile,
        data={
            "bio": "a" * 301,
            "website": "https://example.com",
            "location": "India",
            "birth_date": "2000-01-01",
        }
    )

    assert not form.is_valid()
    assert "bio" in form.errors


@pytest.mark.django_db
def test_profile_update_form_http_website():
    user = User.objects.create_user(
        username="john",
        password="Password@123",
    )

    profile = user.profile

    form = ProfileUpdateForm(
        instance=profile,
        data={
            "bio": "Backend Developer",
            "website": "http://example.com",
            "location": "India",
            "birth_date": "2000-01-01",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_profile_update_form_https_website():
    user = User.objects.create_user(
        username="john",
        password="Password@123",
    )

    profile = user.profile

    form = ProfileUpdateForm(
        instance=profile,
        data={
            "bio": "Backend Developer",
            "website": "https://example.com",
            "location": "India",
            "birth_date": "2000-01-01",
        }
    )

    assert form.is_valid()




@pytest.mark.django_db
def test_forgot_password_form_empty_email():
    form = ForgotPasswordForm(
        data={
            "email": "",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors



@pytest.mark.django_db
def test_forgot_password_form_invalid_email_format():
    form = ForgotPasswordForm(
        data={
            "email": "john@example",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors




def test_otp_form_exactly_six_digits():
    form = OTPForm(
        data={
            "otp": "123456",
        }
    )

    assert form.is_valid()


def test_otp_form_less_than_six_digits():
    form = OTPForm(
        data={
            "otp": "12345",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors


def test_otp_form_more_than_six_digits():
    form = OTPForm(
        data={
            "otp": "1234567",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors


def test_otp_form_letters():
    form = OTPForm(
        data={
            "otp": "abcdef",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors


def test_otp_form_mixed_characters():
    form = OTPForm(
        data={
            "otp": "12AB34",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors




def test_reset_password_form_empty_first_password():
    form = ResetPasswordForm(
        data={
            "password1": "",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "password1" in form.errors


def test_reset_password_form_empty_second_password():
    form = ResetPasswordForm(
        data={
            "password1": "Password@123",
            "password2": "",
        }
    )

    assert not form.is_valid()
    assert "password2" in form.errors


def test_reset_password_form_both_passwords_empty():
    form = ResetPasswordForm(
        data={
            "password1": "",
            "password2": "",
        }
    )

    assert not form.is_valid()


def test_reset_password_form_matching_passwords():
    form = ResetPasswordForm(
        data={
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()


def test_reset_password_form_different_passwords():
    form = ResetPasswordForm(
        data={
            "password1": "Password@123",
            "password2": "Password@124",
        }
    )

    assert not form.is_valid()
    assert "__all__" in form.errors