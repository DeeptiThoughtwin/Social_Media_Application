from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from apps.Stories.models import Story
from apps.Stories.api.serializers  import StorySerializer
from apps.Stories.api.permissions  import IsOwnerOrReadOnly


class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    queryset = Story.objects.all().order_by("-created_at")
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)