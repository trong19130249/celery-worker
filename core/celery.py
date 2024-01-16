from celery import Celery
import os

# from core.tasks.neighbourhood import get_ipv4_address

app = Celery('core')
app.config_from_object('celeryconfig', namespace='CELERY')
app.autodiscover_tasks()
# remoteAddresses = []
# remoteAddresses.append(get_ipv4_address())
message_data = {
    "brand":"metavms",
    "cloudHost":"meta.nxvms.com",
    "cloudSystemId":"",
    "customization":"metavms",
    "ecDbReadOnly":False,
    "hwPlatform":"unknown",
    "id":"{ffa6e103-e93b-4920-8864-460ae246e13b}",
    "localSystemId":"{93aee1e8-f2b7-419f-93be-907c1318914b}",
    "name":"Server oryza Calery docker",
    "port":7002,
    "protoVersion":5107,
    "realm":"VMS",
    "remoteAddresses":["fe80::d8e:d343:e71c:c234%3","d2baacef-78c7-09d0-3c92-ff83a813dc41.82161a01-8f82-4c72-b680-eb1d10464a71","192.168.103.78","172.19.0.3"],
    "runtimeId":"{0e1b6e03-35b5-420d-8f3e-419925ae1d3f}",
    "serverFlags":"SF_HasPublicIP|SF_SupportsTranscoding",
    "sslAllowed":True,
    "synchronizedTimeMs":"",
    "systemName":"Oryza Cloud",
    "type":"Media Server",
    "version":"5.1.0.37133"
}

app.conf.beat_schedule = {
    'send-notification-every-1-seconds': {
        'task': 'core.tasks.tasks.send_notification_task',
        # 5s for testing
        'schedule':5,
        'args': (message_data,),
    },
}
