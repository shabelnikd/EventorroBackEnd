web: gunicorn --bind 0.0.0.0:8000 afiche.wsgi:application
worker: celery -A afiche worker --loglevel=info
beat: celery -A afiche beat --loglevel=info