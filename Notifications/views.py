from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import JsonResponse


@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        receiver=request.user
    ).order_by("-created_at")
    notifications.update(is_read=True)

    return render(
        request,
        "notifications.html",
        {
            "notifications": notifications
        }
    )



@login_required
def notification_count(request):

    count = request.user.received_notifications.filter(
        is_read=False
    ).count()

    return JsonResponse({
        "count": count
    })
