from celery import app


@app.task
def broadcast_task():
    return 'Success broadcast_task'
