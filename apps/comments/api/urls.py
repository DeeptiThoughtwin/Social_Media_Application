from django.urls import path
from apps.comments.api.views import (
    CommentListCreateAPIView,
    DeleteCommentAPIView,
)

urlpatterns = [
    path("posts/<int:pk>/comments/",CommentListCreateAPIView.as_view(),name="comment-list-create"),
    path("comments/<int:pk>/delete/",DeleteCommentAPIView.as_view(),name="comment-delete"),
]