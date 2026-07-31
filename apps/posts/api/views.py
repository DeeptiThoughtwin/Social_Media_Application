from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.posts.models import Post, Like
from apps.posts.api.serializers import PostSerializer,LikeSerializer
from apps.posts.api.permissions import IsOwner
from rest_framework import viewsets



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    # pagination_class = myPagePagination

    def get_permissions(self):

        if self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        if created:
            liked = True
        else:
            like.delete()
            liked = False
        return Response({
            "liked": liked,
            "likes_count": post.likes.count()
        })



class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)