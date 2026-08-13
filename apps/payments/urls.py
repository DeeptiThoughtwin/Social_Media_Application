from django.urls import path

from .views import (
    payment_page,
    create_checkout_session,
    payment_success,
    payment_cancel,
    stripe_webhook,
)


urlpatterns = [
    path(
        "",
        payment_page,
        name="payment_page",
    ),

    path(
        "checkout/",
        create_checkout_session,
        name="create_checkout_session",
    ),

    path(
        "success/",
        payment_success,
        name="payment_success",
    ),

    path(
        "cancel/",
        payment_cancel,
        name="payment_cancel",
    ),

    path(
        "webhook/",
        stripe_webhook,
        name="stripe_webhook",
    ),
]