from django.urls import path
from apps.Notifications.api.views import (
    NotificationListAPIView,
    NotificationCountAPIView,
    MarkNotificationReadAPIView,
    MarkAllNotificationsReadAPIView,
)

urlpatterns = [
    path("",NotificationListAPIView.as_view(),name="notification-list"),
    path("count/",NotificationCountAPIView.as_view(),name="notification-count"),
    path("<int:pk>/read/",MarkNotificationReadAPIView.as_view(),name="notification-read"),
    path("read-all/",MarkAllNotificationsReadAPIView.as_view(),name="notification-read-all"),
]