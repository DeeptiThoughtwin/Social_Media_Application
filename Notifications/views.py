from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Notifications.models import Notification


class NotificationsView(LoginRequiredMixin, TemplateView):
    """Display the user's notification history and mark them as read."""
    template_name = "notifications.html"
    def get_context_data(self, **kwargs):
        """Retrieve notifications and mark unread ones as read."""
        context = super().get_context_data(**kwargs)
        notifications = list(
            Notification.objects.filter(receiver=self.request.user).order_by("-created_at")
        )
        Notification.objects.filter(receiver=self.request.user,is_read=False).update(is_read=True)
        context["notifications"] = notifications
        return context


class NotificationCountView(LoginRequiredMixin, View):
    """Return the number of unread notifications for the current user."""
    def get(self, request, *args, **kwargs):
        count = request.user.received_notifications.filter(is_read=False).count()
        return JsonResponse({"count": count})
