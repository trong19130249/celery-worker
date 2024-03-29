from celery import shared_task

from celeryconfig import MULTICAST_GROUP, MULTICAST_PORT, IP_V4
# from celeryconfig import MULTICAST_GROUP, MULTICAST_PORT
from core.celery import app
import socket
import struct
import json
import time

from core.tasks.neighbourhood import scan_neighbourhood
from core.ultils import get_ipv4_address

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

group = socket.inet_aton(MULTICAST_GROUP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
#                 socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton(IP_V4))
# sock.bind((MULTICAST_GROUP, MULTICAST_PORT))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


@shared_task
def send_notification_task(message):
    message["synchronizedTimeMs"] = str(int(time.time() * 1000))
    message = json.dumps(message)
    sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
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
    return message


@shared_task
def broadcast_scan_network_task():
    results = scan_neighbourhood()
    sock.sendto(json.dumps(results).encode(), (MULTICAST_GROUP, MULTICAST_PORT))
    return results

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("setup_periodic_tasks")
    sender.add_periodic_task(1.0, send_notification_task.s("Hello World"), name="Send notification every 1 seconds")
