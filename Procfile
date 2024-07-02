web: gunicorn gfpgan.wsgi --timeout 10000 --log-file -
worker: celery -A gfpgan worker --loglevel=info