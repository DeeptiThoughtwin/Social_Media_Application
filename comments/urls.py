from django.urls import path
from . import views

urlpatterns = [
    path('comment/<int:pk>/',views.CommentView.as_view(), name='comment_view'),
    path("delete/<int:pk>/",views.DeleteCommentView.as_view(),name="delete_comment"),
]