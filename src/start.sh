python manage.py migrate &&
python manage.py collectstatic --noinput &&
gunicorn service_app.asgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
