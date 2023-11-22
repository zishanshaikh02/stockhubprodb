
import os
import django
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Database.settings")
django.setup()

from images.models import Subscription

scheduler = BackgroundScheduler()

def check_subscription_status():
    current_date = timezone.now().date()
    subscriptions = Subscription.objects.filter(
        expires_in__isnull=False,
        active=True,
        expires_in__lt=current_date,
    )

    for subscription in subscriptions:
        subscription.active = False
        subscription.save()

# Schedule the task to run every minute
scheduler.add_job(check_subscription_status, 'interval', minutes=60)

scheduler.start()
