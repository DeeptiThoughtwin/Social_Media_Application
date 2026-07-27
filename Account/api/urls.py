from django.urls import path
from Account.api.views import HomeAPIView

urlpatterns = [
    path('home/', HomeAPIView.as_view(), name='api-home'),
]
