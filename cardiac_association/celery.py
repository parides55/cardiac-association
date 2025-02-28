import os
from celery import Celery

# Set default settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardiac_association.settings')

app = Celery('cardiac_association')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all Django apps
app.autodiscover_tasks()