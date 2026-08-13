from io import BytesIO
import pytest
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from apps.Stories.models import Story


def create_test_image(name="story.png"):
    image = Image.new("RGB", (100, 100), "red")

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return SimpleUploadedFile(
        name,
        buffer.read(),
        content_type="image/png",
    )


@pytest.mark.django_db
class TestStoryViewSet:

    def test_list_stories(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = create_test_image("story.png")

        Story.objects.create(
            user=user,
            image=image
        )

        client.force_authenticate(user=user)

        response = client.get(
            "/stories/api/stories/"
        )

        assert response.status_code == status.HTTP_200_OK

    def test_create_story(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.force_authenticate(user=user)

        image = create_test_image("story.png")

        response = client.post(
            "/stories/api/stories/",
            {
                "image": image
            },
            format="multipart"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Story.objects.count() == 1

        story = Story.objects.first()

        assert story.user == user
        assert story.image.name.startswith("stories/")

    def test_create_story_without_login(self):
        client = APIClient()

        image = create_test_image("story.png")

        response = client.post(
            "/stories/api/stories/",
            {
                "image": image
            },
            format="multipart"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Story.objects.count() == 0

    def test_retrieve_story(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = create_test_image("story.png")

        story = Story.objects.create(
            user=user,
            image=image
        )

        client.force_authenticate(user=user)

        response = client.get(
            f"/stories/api/stories/{story.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == story.id

    def test_update_own_story(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = create_test_image("story.png")

        story = Story.objects.create(
            user=user,
            image=image
        )

        client.force_authenticate(user=user)

        new_image = create_test_image("new_story.png")

        response = client.patch(
            f"/stories/api/stories/{story.id}/",
            {
                "image": new_image
            },
            format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK

        story.refresh_from_db()

        assert story.user == user
        assert story.image.name.startswith("stories/")

    def test_other_user_cannot_update_story(self):
        client = APIClient()

        owner = User.objects.create_user(
            username="john",
            password="password123"
        )

        other_user = User.objects.create_user(
            username="alex",
            password="password123"
        )

        image = create_test_image("story.png")

        story = Story.objects.create(
            user=owner,
            image=image
        )

        client.force_authenticate(user=other_user)

        new_image = create_test_image("new_story.png")

        response = client.patch(
            f"/stories/api/stories/{story.id}/",
            {
                "image": new_image
            },
            format="multipart"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        story.refresh_from_db()

        assert story.user == owner

    def test_delete_own_story(self):
        client = APIClient()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = create_test_image("story.png")

        story = Story.objects.create(
            user=user,
            image=image
        )

        client.force_authenticate(user=user)

        response = client.delete(
            f"/stories/api/stories/{story.id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Story.objects.count() == 0

    def test_other_user_cannot_delete_story(self):
        client = APIClient()

        owner = User.objects.create_user(
            username="john",
            password="password123"
        )

        other_user = User.objects.create_user(
            username="alex",
            password="password123"
        )

        image = create_test_image("story.png")

        story = Story.objects.create(
            user=owner,
            image=image
        )

        client.force_authenticate(user=other_user)

        response = client.delete(
            f"/stories/api/stories/{story.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Story.objects.count() == 1

