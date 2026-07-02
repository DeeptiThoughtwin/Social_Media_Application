from django.urls import path
from . import views

urlpatterns = [
    path("add/",views.add_story,name="add_story"),
    path("",views.story_list,name="story_list"),
    path("delete/<int:story_id>/",views.delete_story,name="delete_story"),
]