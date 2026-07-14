from django.urls import path
from . import views

urlpatterns = [
    path('comment/<int:pk>/', views.comment_view, name='comment_view'),
    path("delete/<int:pk>/",views.delete_comment,name="delete_comment"),
]
