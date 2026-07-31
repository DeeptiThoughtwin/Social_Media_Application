from rest_framework import serializers
from apps.posts.models import Post, PostMedia,Like



class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ["id", "file", "media_type"]


class PostSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True, read_only=True)
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ["id", "user", "caption", "created_at", "media", "files"]
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        files = validated_data.pop("files", [])
        user = self.context["request"].user
        post = Post.objects.create(user=user,**validated_data)
        for file in files:
            media_type = (
                "video"
                if file.content_type.startswith("video")
                else "image"
            )
            PostMedia.objects.create(
                post=post,
                file=file,
                media_type=media_type
            )
        return post




class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ["user"]