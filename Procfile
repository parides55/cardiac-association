web: gunicorn cardiac_association.wsgi
worker: celery -A cardiac_association worker -P threads --loglevel=info
flower: gunicorn --bind=0.0.0.0:5555 flower:main
