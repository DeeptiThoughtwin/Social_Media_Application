from io import BytesIO
import pytest
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
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
class TestStoryViews:

    def test_add_story_success(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.login(
            username="john",
            password="password123"
        )

        image = create_test_image("story.png")

        response = client.post(
            reverse("add_story"),
            {
                "image": image,
            }
        )

        print("STATUS:", response.status_code)

        if response.context and "form" in response.context:
            print("FORM ERRORS:", response.context["form"].errors)

        assert response.status_code == 302
        assert response.url == reverse("home")

        assert Story.objects.count() == 1

        story = Story.objects.first()

        assert story.user == user
        assert story.image.name.startswith("stories/")
    def test_add_story_get(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        client.login(
            username="john",
            password="password123"
        )

        response = client.get(
            reverse("add_story")
        )

        assert response.status_code == 200
        assert "form" in response.context

    def test_story_list(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = create_test_image("story.png")

        story = Story.objects.create(
            user=user,
            image=image
        )

        client.login(
            username="john",
            password="password123"
        )

        response = client.get(
            reverse("story_list")
        )

        assert response.status_code == 200
        assert story in response.context["stories"]

    def test_delete_story(self, client):
        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        image = create_test_image("story.png")

        story = Story.objects.create(
            user=user,
            image=image
        )

        client.login(
            username="john",
            password="password123"
        )

        response = client.post(
            reverse(
                "delete_story",
                kwargs={"story_id": story.id}
            )
        )

        assert response.status_code == 302
        assert response.url == reverse("home")

        assert Story.objects.count() == 0

    def test_user_cannot_delete_other_users_story(self, client):
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

        client.login(
            username="alex",
            password="password123"
        )

        response = client.post(
            reverse(
                "delete_story",
                kwargs={"story_id": story.id}
            )
        )

        assert response.status_code == 404
        assert Story.objects.count() == 1

