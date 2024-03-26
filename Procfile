web: gunicorn LSDtest1.wsgi:application --timeout 12000 --log-file -
worker: celery -A livesportsdisplay worker --loglevel=info

