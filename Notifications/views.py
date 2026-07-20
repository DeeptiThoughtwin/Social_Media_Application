from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import JsonResponse


@login_required
def notifications(request):
    """Display the user's notification history and mark them as read.

    Queries all notifications where the current authenticated user is the
    receiver, orders them from newest to oldest, and marks all retrieved
    notifications as read in a single batch operation.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered 'notifications.html' template populated 
            with the user's notifications.
    """
    notifications = list(
        Notification.objects.filter(receiver=request.user).order_by("-created_at")
    )
    
    Notification.objects.filter(receiver=request.user, is_read=False).update(is_read=True)

    return render(
        request,
        "notifications.html",
        {
            "notifications": notifications
        }
    )

    


@login_required
def notification_count(request):
    """Get the total number of unread notifications for the current user.

    Queries the database using the user's related notification manager to
    count all incoming notifications that have not been read yet. 

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON object containing the 'count' integer of 
            unread notifications.
    """
    count = request.user.received_notifications.filter(
        is_read=False
    ).count()

    return JsonResponse({
        "count": count
    })


