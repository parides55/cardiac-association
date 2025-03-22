import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardiac_association.settings')

app = Celery('cardiac_association')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()