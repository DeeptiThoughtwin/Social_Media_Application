import pytest
from django.contrib.auth.models import User
from apps.Account.forms import (
    RegistrationForm,
    LoginForm,
    UserUpdateForm,
    ProfileUpdateForm,
    ForgotPasswordForm,
    OTPForm,
    ResetPasswordForm,
)
from apps.Account.models import Profile




@pytest.mark.django_db
def test_registration_form_valid():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_registration_form_creates_user():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()

    user = form.save()

    assert user.username == "john123"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john@example.com"


@pytest.mark.django_db
def test_registration_username_cannot_start_with_number():
    form = RegistrationForm(
        data={
            "username": "123john",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_registration_username_minimum_length():
    form = RegistrationForm(
        data={
            "username": "abc",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_registration_username_maximum_length():
    form = RegistrationForm(
        data={
            "username": "abcdefghijklmnopqrstu",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_registration_username_invalid_characters():
    form = RegistrationForm(
        data={
            "username": "john-doe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_registration_username_duplicate():
    User.objects.create_user(
        username="john123",
        password="Password@123",
    )

    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "new@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_registration_username_is_trimmed():
    form = RegistrationForm(
        data={
            "username": "  john123  ",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()
    assert form.cleaned_data["username"] == "john123"


@pytest.mark.django_db
def test_registration_first_name_minimum_length():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "J",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "first_name" in form.errors


@pytest.mark.django_db
def test_registration_first_name_cannot_start_with_number():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "1John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "first_name" in form.errors


@pytest.mark.django_db
def test_registration_first_name_invalid_characters():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John123",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "first_name" in form.errors


@pytest.mark.django_db
def test_registration_first_name_is_title_case():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "john",
            "last_name": "doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()

    assert form.cleaned_data["first_name"] == "John"
    assert form.cleaned_data["last_name"] == "Doe"


@pytest.mark.django_db
def test_registration_last_name_minimum_length():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "D",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "last_name" in form.errors


@pytest.mark.django_db
def test_registration_last_name_cannot_start_with_number():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "1Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "last_name" in form.errors


@pytest.mark.django_db
def test_registration_last_name_invalid_characters():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe123",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "last_name" in form.errors


@pytest.mark.django_db
def test_registration_duplicate_email():
    User.objects.create_user(
        username="existing",
        email="john@example.com",
        password="Password@123",
    )

    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_registration_email_is_lowercase():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "JOHN@EXAMPLE.COM",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()
    assert form.cleaned_data["email"] == "john@example.com"


@pytest.mark.django_db
def test_registration_password_minimum_length():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Pass@1",
            "password2": "Pass@1",
        }
    )

    assert not form.is_valid()
    assert "password1" in form.errors


@pytest.mark.django_db
def test_registration_password_requires_uppercase():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "password@123",
            "password2": "password@123",
        }
    )

    assert not form.is_valid()
    assert "password1" in form.errors


@pytest.mark.django_db
def test_registration_password_requires_lowercase():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "PASSWORD@123",
            "password2": "PASSWORD@123",
        }
    )

    assert not form.is_valid()
    assert "password1" in form.errors


@pytest.mark.django_db
def test_registration_password_requires_number():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@",
            "password2": "Password@",
        }
    )

    assert not form.is_valid()
    assert "password1" in form.errors


@pytest.mark.django_db
def test_registration_password_requires_special_character():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password123",
            "password2": "Password123",
        }
    )

    assert not form.is_valid()
    assert "password1" in form.errors


@pytest.mark.django_db
def test_registration_passwords_must_match():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Different@123",
        }
    )

    assert not form.is_valid()
    assert "password2" in form.errors


# ============================================================
# Login Form
# ============================================================


@pytest.mark.django_db
def test_login_form_valid():
    User.objects.create_user(
        username="john",
        password="Password@123",
    )

    form = LoginForm(
        data={
            "username": "john",
            "password": "Password@123",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_password():
    User.objects.create_user(
        username="john",
        password="Password@123",
    )

    form = LoginForm(
        data={
            "username": "john",
            "password": "WrongPassword@123",
        }
    )

    assert not form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_username():
    form = LoginForm(
        data={
            "username": "unknown",
            "password": "Password@123",
        }
    )

    assert not form.is_valid()





@pytest.mark.django_db
def test_user_update_form_valid():
    user = User.objects.create_user(
        username="john",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="Password@123",
    )

    form = UserUpdateForm(
        instance=user,
        data={
            "first_name": "Alice",
            "last_name": "Smith",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_user_update_form_saves_names():
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
            "last_name": "Smith",
        }
    )

    assert form.is_valid()

    updated_user = form.save()

    assert updated_user.first_name == "Alice"
    assert updated_user.last_name == "Smith"


@pytest.mark.django_db
def test_user_update_form_allows_same_email():
    user = User.objects.create_user(
        username="john",
        email="john@example.com",
        password="Password@123",
    )

    form = UserUpdateForm(
        instance=user,
        data={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
        }
    )

    assert form.is_valid()





@pytest.mark.django_db
def test_profile_update_form_valid():
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
def test_profile_update_form_saves_data():
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

    updated_profile = form.save()

    assert updated_profile.bio == "Backend Developer"
    assert updated_profile.website == "https://example.com"
    assert updated_profile.location == "India"


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
            "website": "not-a-valid-url",
            "location": "India",
            "birth_date": "2000-01-01",
        }
    )

    assert not form.is_valid()
    assert "website" in form.errors


@pytest.mark.django_db
def test_profile_update_form_bio_max_length():
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
def test_forgot_password_form_valid():
    User.objects.create_user(
        username="john",
        email="john@example.com",
        password="Password@123",
    )

    form = ForgotPasswordForm(
        data={
            "email": "john@example.com",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_forgot_password_form_invalid_email():
    form = ForgotPasswordForm(
        data={
            "email": "not-an-email",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_forgot_password_form_unknown_email():
    form = ForgotPasswordForm(
        data={
            "email": "unknown@example.com",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_forgot_password_form_returns_email():
    User.objects.create_user(
        username="john",
        email="john@example.com",
        password="Password@123",
    )

    form = ForgotPasswordForm(
        data={
            "email": "john@example.com",
        }
    )

    assert form.is_valid()
    assert form.cleaned_data["email"] == "john@example.com"





def test_otp_form_valid():
    form = OTPForm(
        data={
            "otp": "123456",
        }
    )

    assert form.is_valid()


def test_otp_form_invalid_characters():
    form = OTPForm(
        data={
            "otp": "12AB56",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors


def test_otp_form_invalid_special_characters():
    form = OTPForm(
        data={
            "otp": "123@56",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors


def test_otp_form_empty():
    form = OTPForm(
        data={
            "otp": "",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors


def test_otp_form_maximum_six_digits():
    form = OTPForm(
        data={
            "otp": "1234567",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors





def test_reset_password_form_valid():
    form = ResetPasswordForm(
        data={
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()


def test_reset_password_form_passwords_do_not_match():
    form = ResetPasswordForm(
        data={
            "password1": "Password@123",
            "password2": "Different@123",
        }
    )

    assert not form.is_valid()
    assert "__all__" in form.errors





@pytest.mark.django_db
def test_registration_username_exactly_minimum_length():
    form = RegistrationForm(
        data={
            "username": "john",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_registration_username_with_underscore():
    form = RegistrationForm(
        data={
            "username": "john_123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_registration_username_with_spaces_is_cleaned():
    form = RegistrationForm(
        data={
            "username": "  john123  ",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()
    assert form.cleaned_data["username"] == "john123"


@pytest.mark.django_db
def test_registration_first_name_is_trimmed():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "  john  ",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()
    assert form.cleaned_data["first_name"] == "John"


@pytest.mark.django_db
def test_registration_last_name_is_trimmed():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "  doe  ",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()
    assert form.cleaned_data["last_name"] == "Doe"


@pytest.mark.django_db
def test_registration_email_with_spaces_is_cleaned():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "  john@example.com  ",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()
    assert form.cleaned_data["email"] == "john@example.com"


@pytest.mark.django_db
def test_registration_email_case_is_normalized():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "JOHN@EXAMPLE.COM",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert form.is_valid()
    assert form.cleaned_data["email"] == "john@example.com"


@pytest.mark.django_db
def test_registration_missing_username():
    form = RegistrationForm(
        data={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_registration_missing_email():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "Password@123",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_registration_missing_password():
    form = RegistrationForm(
        data={
            "username": "john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "",
            "password2": "",
        }
    )

    assert not form.is_valid()
    assert "password1" in form.errors





@pytest.mark.django_db
def test_login_form_empty_username():
    form = LoginForm(
        data={
            "username": "",
            "password": "Password@123",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_login_form_empty_password():
    form = LoginForm(
        data={
            "username": "john",
            "password": "",
        }
    )

    assert not form.is_valid()
    assert "password" in form.errors


@pytest.mark.django_db
def test_login_form_username_is_trimmed():
    User.objects.create_user(
        username="john",
        password="Password@123",
    )

    form = LoginForm(
        data={
            "username": "  john  ",
            "password": "Password@123",
        }
    )

    assert form.is_valid()






@pytest.mark.django_db
def test_user_update_form_first_name_update():
    user = User.objects.create_user(
        username="john",
        first_name="Old",
        last_name="Name",
        password="Password@123",
    )

    form = UserUpdateForm(
        instance=user,
        data={
            "first_name": "New",
            "last_name": "Name",
        }
    )

    assert form.is_valid()

    form.save()

    user.refresh_from_db()

    assert user.first_name == "New"





@pytest.mark.django_db
def test_profile_update_form_empty_bio():
    user = User.objects.create_user(
        username="john",
        password="Password@123",
    )

    profile = user.profile

    form = ProfileUpdateForm(
        instance=profile,
        data={
            "bio": "",
            "website": "https://example.com",
            "location": "India",
            "birth_date": "2000-01-01",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_profile_update_form_empty_location():
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
            "location": "",
            "birth_date": "2000-01-01",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_profile_update_form_empty_website():
    user = User.objects.create_user(
        username="john",
        password="Password@123",
    )

    profile = user.profile

    form = ProfileUpdateForm(
        instance=profile,
        data={
            "bio": "Backend Developer",
            "website": "",
            "location": "India",
            "birth_date": "2000-01-01",
        }
    )

    assert form.is_valid()





@pytest.mark.django_db
def test_forgot_password_email_with_spaces():
    User.objects.create_user(
        username="john",
        email="john@example.com",
        password="Password@123",
    )

    form = ForgotPasswordForm(
        data={
            "email": "  john@example.com  ",
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


def test_otp_form_seven_digits():
    form = OTPForm(
        data={
            "otp": "1234567",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors


def test_otp_form_whitespace():
    form = OTPForm(
        data={
            "otp": "123 56",
        }
    )

    assert not form.is_valid()
    assert "otp" in form.errors





def test_reset_password_form_first_password_empty():
    form = ResetPasswordForm(
        data={
            "password1": "",
            "password2": "Password@123",
        }
    )

    assert not form.is_valid()


def test_reset_password_form_second_password_empty():
    form = ResetPasswordForm(
        data={
            "password1": "Password@123",
            "password2": "",
        }
    )

    assert not form.is_valid()


def test_reset_password_form_different_passwords():
    form = ResetPasswordForm(
        data={
            "password1": "Password@123",
            "password2": "Password@124",
        }
    )

    assert not form.is_valid()
    assert "__all__" in form.errors