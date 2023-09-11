from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User


def send_contact_email_message(subject, email, content, user_id):
    """
    Function to send contact form email
    """
    user = User.objects.get(id=user_id) if user_id else None
    message = render_to_string('main/email/feedback_email_send.html', {
        'email': email,
        'content': content,
        'user': user,
    })
    send_mail(
        subject,
        message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['lionheartbow@yandex.ru'],
        fail_silently=False
    )
    # email = EmailMessage(subject, message, settings.EMAIL_HOST_, settings.EMAIL_HOST_USER,)
    # email.send(fail_silently=False)