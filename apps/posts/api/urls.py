from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.posts.api.views import PostViewSet,LikeViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("likes", LikeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]





