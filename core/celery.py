from celery import Celery
import os



app = Celery('core')
app.config_from_object('celeryconfig', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-notification-every-1-seconds': {
        'task': 'core.tasks.tasks.send_notification_task',
        # 5s for testing
        'schedule':5,
        'args': ('Hello World',),
    },
}
