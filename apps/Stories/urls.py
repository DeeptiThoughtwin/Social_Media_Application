from django.urls import path
from . import views

urlpatterns = [
    path("", views.StoryListView.as_view(), name="story_list"),
    path("add/", views.AddStoryView.as_view(), name="add_story"),
    path("delete/<int:story_id>/", views.DeleteStoryView.as_view(), name="delete_story"),
]
