import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone
from apps.Account.models import Profile, Follow, PasswordResetOTP
User = get_user_model()


@pytest.mark.django_db
def test_profile_is_created_for_new_user():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    assert Profile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_profile_has_correct_user():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    profile = user.profile

    assert profile.user == user


@pytest.mark.django_db
def test_profile_bio_can_be_updated():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    profile = user.profile

    profile.bio = "Django Developer"
    profile.save()

    profile.refresh_from_db()

    assert profile.bio == "Django Developer"


@pytest.mark.django_db
def test_profile_website_can_be_updated():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    profile = user.profile

    profile.website = "https://example.com"
    profile.save()

    profile.refresh_from_db()

    assert profile.website == "https://example.com"


@pytest.mark.django_db
def test_profile_location_can_be_updated():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    profile = user.profile

    profile.location = "India"
    profile.save()

    profile.refresh_from_db()

    assert profile.location == "India"


@pytest.mark.django_db
def test_profile_updated_at_changes_after_update():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    profile = user.profile

    old_updated_at = profile.updated_at

    profile.bio = "New Bio"
    profile.save()

    profile.refresh_from_db()

    assert profile.updated_at >= old_updated_at


@pytest.mark.django_db
def test_profile_belongs_to_one_user():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    profile = user.profile

    assert profile.user_id == user.id


@pytest.mark.django_db
def test_profile_is_deleted_when_user_is_deleted():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    profile_id = user.profile.id

    user.delete()

    assert not Profile.objects.filter(id=profile_id).exists()




@pytest.mark.django_db
def test_follow_count():
    user1 = User.objects.create_user(
        username="john",
        password="123"
    )

    user2 = User.objects.create_user(
        username="alice",
        password="123"
    )

    Follow.objects.create(
        follower=user1,
        following=user2
    )

    assert Follow.objects.count() == 1


@pytest.mark.django_db
def test_follower_relationship():
    user1 = User.objects.create_user(
        username="john",
        password="123"
    )

    user2 = User.objects.create_user(
        username="alice",
        password="123"
    )

    follow = Follow.objects.create(
        follower=user1,
        following=user2
    )

    assert follow.follower.username == "john"
    assert follow.following.username == "alice"


@pytest.mark.django_db
def test_user_can_follow_multiple_users():
    user1 = User.objects.create_user(
        username="john",
        password="123"
    )

    user2 = User.objects.create_user(
        username="alice",
        password="123"
    )

    user3 = User.objects.create_user(
        username="zack",
        password="123"
    )

    Follow.objects.create(
        follower=user1,
        following=user2
    )

    Follow.objects.create(
        follower=user1,
        following=user3
    )

    assert Follow.objects.filter(
        follower=user1
    ).count() == 2


@pytest.mark.django_db
def test_user_can_have_multiple_followers():
    user1 = User.objects.create_user(
        username="john",
        password="123"
    )

    user2 = User.objects.create_user(
        username="alice",
        password="123"
    )

    user3 = User.objects.create_user(
        username="zack",
        password="123"
    )

    Follow.objects.create(
        follower=user2,
        following=user1
    )

    Follow.objects.create(
        follower=user3,
        following=user1
    )

    assert Follow.objects.filter(
        following=user1
    ).count() == 2


@pytest.mark.django_db
def test_follow_can_be_deleted():
    user1 = User.objects.create_user(
        username="john",
        password="123"
    )

    user2 = User.objects.create_user(
        username="alice",
        password="123"
    )

    follow = Follow.objects.create(
        follower=user1,
        following=user2
    )

    follow.delete()

    assert not Follow.objects.filter(
        follower=user1,
        following=user2
    ).exists()


@pytest.mark.django_db
def test_follow_relationship_exists():
    user1 = User.objects.create_user(
        username="john",
        password="123"
    )

    user2 = User.objects.create_user(
        username="alice",
        password="123"
    )

    Follow.objects.create(
        follower=user1,
        following=user2
    )

    assert Follow.objects.filter(
        follower=user1,
        following=user2
    ).exists()


@pytest.mark.django_db
def test_same_user_cannot_follow_twice():
    user1 = User.objects.create_user(
        username="john",
        password="123"
    )

    user2 = User.objects.create_user(
        username="alice",
        password="123"
    )

    Follow.objects.create(
        follower=user1,
        following=user2
    )

    with pytest.raises(IntegrityError):
        Follow.objects.create(
            follower=user1,
            following=user2
        )




@pytest.mark.django_db
def test_password_reset_otp_belongs_to_user():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    otp = PasswordResetOTP.objects.create(
        user=user,
        otp="123456"
    )

    assert otp.user == user


@pytest.mark.django_db
def test_password_reset_otp_is_saved():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    PasswordResetOTP.objects.create(
        user=user,
        otp="123456"
    )

    assert PasswordResetOTP.objects.filter(
        user=user
    ).exists()


@pytest.mark.django_db
def test_password_reset_otp_can_be_updated():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    otp = PasswordResetOTP.objects.create(
        user=user,
        otp="123456"
    )

    otp.otp = "654321"
    otp.save()

    otp.refresh_from_db()

    assert otp.otp == "654321"


@pytest.mark.django_db
def test_password_reset_otp_created_at_is_valid():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    before = timezone.now()

    otp = PasswordResetOTP.objects.create(
        user=user,
        otp="123456"
    )

    after = timezone.now()

    assert before <= otp.created_at <= after


@pytest.mark.django_db
def test_password_reset_otp_can_be_deleted():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    otp = PasswordResetOTP.objects.create(
        user=user,
        otp="123456"
    )

    otp_id = otp.id

    otp.delete()

    assert not PasswordResetOTP.objects.filter(
        id=otp_id
    ).exists()


@pytest.mark.django_db
def test_password_reset_otp_str_uses_username():
    user = User.objects.create_user(
        username="john",
        password="password123"
    )

    otp = PasswordResetOTP.objects.create(
        user=user,
        otp="123456"
    )

    assert str(otp) == user.username

