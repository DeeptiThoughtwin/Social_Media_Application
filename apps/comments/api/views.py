from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.posts.models import Post
from apps.comments.models import Comment
from apps.comments.api.serializers import CommentSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        return Comment.objects.filter(
            post_id=post_id,
            active=True
        ).order_by("created_on")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])

        parent = None
        parent_id = self.request.data.get("parent")

        if parent_id:
            parent = get_object_or_404(Comment, pk=parent_id)

        serializer.save(
            author=self.request.user,
            post=post,
            parent=parent
        )


class DeleteCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if request.user == comment.author or request.user == comment.post.user:
            comment.delete()
            return Response(
                {"message": "Comment deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {"error": "Permission denied"},
            status=status.HTTP_403_FORBIDDEN
        )