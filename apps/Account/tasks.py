from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


# @shared_task
# def send_welcome_email(username, email):
#     send_mail(
#         subject="Welcome to My App",
#         message=f"Hi {username},\n\nWelcome to our Django app!",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email],
#         fail_silently=False,
#     )



@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, username, email):
    try:
        print("Trying to send email...")

        raise Exception("Internet Error")

        send_mail(
            subject="Welcome to My App",
            message=f"Hi {username},\n\nWelcome to our Django app!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

    except Exception as exc:
        print("Failed! Retrying in 5 seconds...")

        raise self.retry(
            exc=exc,
            countdown=5
        )