from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.Notifications.models import Notification
from apps.Notifications.api.serializers import NotificationSerializer


class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            receiver=self.request.user).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.filter(is_read=False).update(is_read=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NotificationCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(receiver=request.user,is_read=False).count()
        return Response({
            "unread_count": count
        })


class MarkNotificationReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk,receiver=request.user)
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification not found"},
                status=404
            )
        notification.is_read = True
        notification.save()

        return Response({
            "message": "Notification marked as read"
        })


class MarkAllNotificationsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        Notification.objects.filter(receiver=request.user,is_read=False).update(is_read=True)

        return Response({
            "message": "All notifications marked as read"
        })