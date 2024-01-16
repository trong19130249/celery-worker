import socket
import struct
import json
import time

MULTICAST_GROUP = '239.255.11.11'
MULTICAST_PORT = 7001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

group = socket.inet_aton(MULTICAST_GROUP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock.bind((MULTICAST_GROUP, MULTICAST_PORT))
message_data = {
    "brand":"metavms",
    "cloudHost":"meta.nxvms.com",
    "cloudSystemId":"",
    "customization":"metavms",
    "ecDbReadOnly":False,
    "hwPlatform":"unknown",
    "id":"{ffa6e103-e93b-4920-8864-460ae246e13b}",
    "localSystemId":"{93aee1e8-f2b7-419f-93be-907c1318914b}",
    "name":"Server oryza",
    "port":7002,
    "protoVersion":5107,
    "realm":"VMS",
    "remoteAddresses":["fe80::d8e:d343:e71c:c234%3","d2baacef-78c7-09d0-3c92-ff83a813dc41.82161a01-8f82-4c72-b680-eb1d10464a71","192.168.103.78","14.224.162.5"],
    "runtimeId":"{0e1b6e03-35b5-420d-8f3e-419925ae1d3f}",
    "serverFlags":"SF_HasPublicIP|SF_SupportsTranscoding",
    "sslAllowed":True,
    "synchronizedTimeMs":"",
    "systemName":"Oryza Cloud",
    "type":"Media Server",
    "version":"5.1.0.37133"
}


while True:
    message_data["synchronizedTimeMs"] = str(int(time.time() * 1000))
    print("============================")
    message = json.dumps(message_data)
    sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
    time.sleep(1)

