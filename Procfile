web: gunicorn LSDtest1.wsgi:application --timeout 12000 --log-file -
worker: celery -A LSDtest1 worker --loglevel=info

