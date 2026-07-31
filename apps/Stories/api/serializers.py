from rest_framework import serializers
from apps.Stories.models import Story


class StorySerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Story
        fields = [
            "id",
            "username",
            "user",
            "image",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "username",
            "created_at",
        ]