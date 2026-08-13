from base64 import b64decode

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.Stories.models import Story

VALID_IMAGE = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScL9nAAAAABJRU5ErkJggg=="
)

@pytest.mark.django_db
class TestStoryModel:

    def test_create_story(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = SimpleUploadedFile(
            "story.png",
            VALID_IMAGE,
            content_type="image/png"
        )

        story = Story.objects.create(
            user=user,
            image=image
        )

        assert story.user == user
        assert story.image.name.startswith("stories/")
        assert Story.objects.count() == 1

    def test_story_str(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = SimpleUploadedFile(
            "story.png",
            VALID_IMAGE,
            content_type="image/png"
        )

        story = Story.objects.create(
            user=user,
            image=image
        )

        assert str(story) == "john"

    def test_story_belongs_to_user(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = SimpleUploadedFile(
            "story.png",
            VALID_IMAGE,
            content_type="image/png"
        )

        story = Story.objects.create(
            user=user,
            image=image
        )

        assert story.user.username == "john"

    def test_user_can_have_multiple_stories(self):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image1 = SimpleUploadedFile(
            "story1.png",
            VALID_IMAGE,
            content_type="image/png"
        )

        image2 = SimpleUploadedFile(
            "story2.png",
            VALID_IMAGE,
            content_type="image/png"
        )

        Story.objects.create(
            user=user,
            image=image1
        )

        Story.objects.create(
            user=user,
            image=image2
        )

        assert user.stories.count() == 2
