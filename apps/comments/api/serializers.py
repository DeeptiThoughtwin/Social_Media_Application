from rest_framework import serializers
from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = [
            "id","post","author","body","created_on","active","parent",
        ]
        read_only_fields = [
                "author", "created_on", "post", "parent",
        ]
