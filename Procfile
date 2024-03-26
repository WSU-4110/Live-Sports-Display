web: gunicorn LSDtest1.wsgi:application --timeout 12000 --log-file -
worker: celery -A your_project_name worker --loglevel=info

