from celery import shared_task


from core.celery import app


@shared_task
def send_notification_task(message):
    print(message)

    # channel_layer = get_channel_layer()
    #  print log ra terminal logger
    # async_to_sync(channel_layer.group_send)(
    #     "notifications",
    #     {
    #         "type": "send_notification",
    #         "message": message
    #     }
    # )
    # gửi lên broadcast group notifications

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("setup_periodic_tasks")
    sender.add_periodic_task(1.0, send_notification_task.s("Hello World"), name="Send notification every 1 seconds")
