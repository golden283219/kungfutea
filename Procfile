release: python manage.py collectstatic --noinput
release: python manage.py migrate
web: daphne config.asgi:application -b 0.0.0.0 --port=$PORT
worker: celery worker -A config --beat
