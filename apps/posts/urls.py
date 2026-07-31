from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreatePostView.as_view(), name="create_post"),
    path("like/<int:post_id>/",views.LikePostView.as_view(),name="like_post"),
    path("post/<int:post_id>/",views.PostDetailView.as_view(),name="post_detail"),
    path("edit/<int:pk>/",views.EditPostView.as_view(),name="edit_post"),
    path("delete/<int:pk>/",views.DeletePostView.as_view(),name="delete_post"),

]