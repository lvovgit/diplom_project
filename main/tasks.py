from django.conf import settings
from django.core.mail import send_mail

from core.celery import app
from users.models import User


@app.task
def send_email():
    """Задание периодической отправки сообщения"""
    users = User.objects.all()
    post_list_url = 'http://127.0.0.1:8000/blog/'
    send_mail(
        subject='Ежедневный дайджест',
        message=f'Ознакомьтесь с последними новостями: {post_list_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=users,
        fail_silently=False
    )
