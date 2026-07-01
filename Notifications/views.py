from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications(request):
    notifications = Notification.objects.filter(receiver=request.user).order_by("-created_at")
    return render(request,"notifications.html",{"notifications": notifications})