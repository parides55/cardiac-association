web: gunicorn cardiac_association.wsgi
worker: celery -A cardiac_association worker -P threads --loglevel=info
flower: celery -A cardiac_association flower --port=5555 --broker=$(REDIS_URL)
