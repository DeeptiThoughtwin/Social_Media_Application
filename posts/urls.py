from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/', views.comment_thread, name='comment_thread'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
]



