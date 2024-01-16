import socket
import struct

MULTICAST_GROUP = '239.255.11.11'
MULTICAST_PORT = 7001

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Allow multiple sockets to use the same PORT number
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to the port that we know will receive multicast data
sock.bind((MULTICAST_GROUP, MULTICAST_PORT))

# Tell the kernel that we are a multicast socket
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 

# Tell the kernel that we want to add ourselves to a multicast group
# The address for the multicast group is the third argument
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    print(sock.recv(10240))