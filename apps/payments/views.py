import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Payment


stripe.api_key = settings.STRIPE_SECRET_KEY


# ============================================================
# Payment Page
# ============================================================

@login_required
def payment_page(request):

    return render(
        request,
        "payment.html",
    )


# ============================================================
# Create Stripe Checkout Session
# ============================================================

@login_required
def create_checkout_session(request):

    if request.method != "POST":
        return redirect("payment_page")

    # ₹499 = 49900 paise
    amount = 49900

    # Create pending payment
    payment = Payment.objects.create(
        user=request.user,
        amount=amount,
        currency="inr",
        status="pending",
    )

    # Create Stripe Checkout Session
    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[
            {
                "price_data": {
                    "currency": "inr",

                    "product_data": {
                        "name": "Premium Membership",
                    },

                    "unit_amount": amount,
                },

                "quantity": 1,
            }
        ],

        mode="payment",

        # Successful payment
        success_url=(
            request.build_absolute_uri(
                reverse("profile")
            )
            + "?session_id={CHECKOUT_SESSION_ID}"
        ),

        # Cancelled payment
        cancel_url=request.build_absolute_uri(
            reverse("payment_cancel")
        ),

        # Store our database information in Stripe
        metadata={
            "payment_id": str(payment.id),
            "user_id": str(request.user.id),
        },
    )

    # Save Stripe Checkout Session ID
    payment.stripe_checkout_session_id = session.id

    payment.save(
        update_fields=[
            "stripe_checkout_session_id",
        ]
    )

    # Redirect user to Stripe Checkout
    return redirect(session.url)


# ============================================================
# Payment Success
# ============================================================

@login_required
def payment_success(request):

    session_id = request.GET.get("session_id")

    return render(
        request,
        "payment_success.html",
        {
            "session_id": session_id,
        },
    )


# ============================================================
# Payment Cancel
# ============================================================

@login_required
def payment_cancel(request):

    return render(
        request,
        "payment_cancel.html",
    )
# ============================================================
# Stripe Webhook
# ============================================================

@csrf_exempt
def stripe_webhook(request):

    # Webhook must only accept POST
    if request.method != "POST":
        return HttpResponse(
            "Method not allowed",
            status=405,
        )

    # Get raw Stripe request body
    payload = request.body

    # Get Stripe signature
    sig_header = request.META.get(
        "HTTP_STRIPE_SIGNATURE"
    )

    # --------------------------------------------------------
    # Verify webhook signature
    # --------------------------------------------------------

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )

    except ValueError:
        return HttpResponse(
            "Invalid payload",
            status=400,
        )

    except stripe.error.SignatureVerificationError:
        return HttpResponse(
            "Invalid signature",
            status=400,
        )

    # --------------------------------------------------------
    # Only process checkout.session.completed
    # --------------------------------------------------------

    if event["type"] != "checkout.session.completed":
        return HttpResponse(status=200)

    # --------------------------------------------------------
    # Get Checkout Session
    # --------------------------------------------------------

    session = event["data"]["object"]

    # --------------------------------------------------------
    # Get metadata
    # --------------------------------------------------------

    metadata = session.get("metadata", {})

    payment_id = metadata.get("payment_id")

    if not payment_id:
        return HttpResponse(
            "Payment ID missing",
            status=400,
        )

    # --------------------------------------------------------
    # Find Payment
    # --------------------------------------------------------

    payment = Payment.objects.filter(
        id=payment_id
    ).first()

    if not payment:
        return HttpResponse(
            "Payment not found",
            status=404,
        )

    # --------------------------------------------------------
    # Mark Payment as Paid
    # --------------------------------------------------------

    payment.status = "paid"

    payment.stripe_payment_intent_id = session.get(
        "payment_intent"
    )

    payment.stripe_event_id = event["id"]

    payment.save(
        update_fields=[
            "status",
            "stripe_payment_intent_id",
            "stripe_event_id",
            "updated_at",
        ]
    )

    # --------------------------------------------------------
    # Mark User as Verified
    # --------------------------------------------------------

    profile = payment.user.profile

    profile.is_verified = True

    profile.save(
        update_fields=[
            "is_verified",
        ]
    )

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    return HttpResponse(status=200)