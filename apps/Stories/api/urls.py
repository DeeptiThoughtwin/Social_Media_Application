from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.Stories.api.views import StoryViewSet

router = DefaultRouter()
router.register("stories", StoryViewSet, basename="stories")

urlpatterns = [
    path("", include(router.urls)),
]