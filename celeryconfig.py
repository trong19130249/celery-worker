# Celery configuration
# http://docs.celeryproject.org/en/latest/configuration.html
import os

# from dotenv import load_dotenv
# load_dotenv()


CELERY_IMPORTS =('core.tasks.tasks',)

BROKER_URL = os.environ.get("CELERY_BROKER", "amqp://guest:guest@rabbitmq:5672/")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")