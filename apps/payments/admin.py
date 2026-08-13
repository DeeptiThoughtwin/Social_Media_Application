from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "currency",
        "status",
        "stripe_checkout_session_id",
        "created_at",
    )

    list_filter = (
        "status",
        "currency",
        "created_at",
    )

    search_fields = (
        "user__username",
        "stripe_checkout_session_id",
        "stripe_payment_intent_id",
    )

    readonly_fields = (
        "stripe_checkout_session_id",
        "stripe_payment_intent_id",
        "created_at",
        "updated_at",
    )