uvicorn core.asgi:application --port 8001 --workers 4 --log-level debug --reload
celery -A core beatcelery -A core beat
celery -A core beat -l INFO