from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import MidUser

@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = MidUser.objects.filter(last_login__lt=one_month_ago, status='ac')
    for user in inactive_users:
        user.status = 'inac'
        user.save()
    return f"{inactive_users.count()} users set to inactive"