python manage.py migrate &&
python manage.py collectstatic --noinput &&
gunicorn web.asgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
