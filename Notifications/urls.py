from django.urls import path
from . import views

urlpatterns = [
	path('',views.notifications, name='notifications'),
	path("count/",views.notification_count,name="notification_count"),
]
