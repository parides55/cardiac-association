release: python manage.py migrate  # Runs migrations when deploying
web: gunicorn cardiac_association.wsgi
worker: python manage.py process_tasks