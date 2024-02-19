# Celery configuration
# http://docs.celeryproject.org/en/latest/configuration.html
import os

from dotenv import load_dotenv

from core.ultils import get_ipv4_address

if os.environ.get("ENVIRONMENT",'development') == "development":
    load_dotenv()

CELERY_IMPORTS =('core.tasks.tasks',)

BROKER_URL = os.environ.get("CELERY_BROKER", "amqp://guest:guest@rabbitmq:5672/")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")

MULTICAST_GROUP = os.environ.get("MULTICAST_GROUP", '239.255.11.11')
MULTICAST_PORT = int(os.environ.get("MULTICAST_PORT", 5008))
IP_V4 = get_ipv4_address()

broker_connection_retry_on_startup = True