import logging

from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from apps.Notifications.models import Notification


logger = logging.getLogger(__name__)


class NotificationsView(LoginRequiredMixin, TemplateView):
    """Display the user's notification history and mark them as read."""
    template_name = "notifications.html"

    def get_context_data(self, **kwargs):
        """Retrieve notifications and mark unread ones as read."""
        context = super().get_context_data(**kwargs)

        notifications = list(
            Notification.objects
            .filter(receiver=self.request.user)
            .order_by("-created_at")
        )

        unread_count = Notification.objects.filter(
            receiver=self.request.user,
            is_read=False
        ).count()

        Notification.objects.filter(
            receiver=self.request.user,
            is_read=False
        ).update(is_read=True)

        logger.info(
            "Notifications viewed: user_id=%s total=%s marked_as_read=%s",
            self.request.user.id,
            len(notifications),
            unread_count,
        )

        context["notifications"] = notifications

        return context


class NotificationCountView(LoginRequiredMixin, View):
    """Return the number of unread notifications for the current user."""

    def get(self, request, *args, **kwargs):
        count = request.user.received_notifications.filter(
            is_read=False
        ).count()

        logger.info(
            "Unread notification count requested: user_id=%s count=%s",
            request.user.id,
            count,
        )

        return JsonResponse({"count": count})