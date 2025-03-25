release: python manage.py migrate  # Runs migrations when deploying
web: gunicorn cardiac_association.wsgi
worker: celery -A cardiac_association worker -P threads --loglevel=info
beat: celery -A cardiac_association beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
flower: celery -A cardiac_association flower --port=5555 --broker=$(REDIS_URL)
