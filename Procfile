gunicorn afiche.wsgi --log-file -
worker: celery -A afiche worker --loglevel=info
beat: celery -A afiche beat --loglevel=info