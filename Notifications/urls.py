from django.urls import path
from . import views

urlpatterns = [
    path("",views.NotificationsView.as_view(),name="notifications"),
    path("count/",views.NotificationCountView.as_view(),name="notification_count"),
]