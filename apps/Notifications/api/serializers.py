from rest_framework import serializers
from apps.Notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.username")
    receiver = serializers.ReadOnlyField(source="receiver.username")

    class Meta:
        model = Notification
        fields = [
            "id","sender","receiver","post","notification_type","is_read","created_at",
        ]
        read_only_fields = [
            "sender","receiver","created_at",
        ]