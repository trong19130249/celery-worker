# scan network for devices and print their ip addresses and mac addresses and metadata
# input: network address  192.168.103.11/24

import argparse
from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether, ARP

def arp_scan(ip):
    """
    Performs a network scan by sending ARP requests to an IP address or a range of IP addresses.

    Args:
        ip (str): An IP address or IP address range to scan. For example:
                    - 192.168.1.1 to scan a single IP address
                    - 192.168.1.1/24 to scan a range of IP addresses.

    Returns:
        A list of dictionaries mapping IP addresses to MAC addresses. For example:
        [
            {'IP': '192.168.2.1', 'MAC': 'c4:93:d9:8b:3e:5a'}
        ]
    """
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

    ans, unans = srp(request, timeout=2, retry=1, verbose=True)
    result = []

    for sent, received in ans:
        result.append({'IP': received.psrc, 'MAC': received.hwsrc})

    return result


def tcp_scan(ip, ports):
    """
    Performs a TCP scan by sending SYN packets to <ports>.

    Args:
        ip (str): An IP address or hostname to target.
        ports (list or tuple of int): A list or tuple of ports to scan.

    Returns:
        A list of ports that are open.
    """
    try:
        syn = IP(dst=ip) / TCP(dport=ports, flags="S")
    except socket.gaierror:
        raise ValueError('Hostname {} could not be resolved.'.format(ip))

    ans, unans = sr(syn, timeout=2, retry=1)
    result = []

    for sent, received in ans:
        if received[TCP].flags == "SA":
            result.append(received[TCP].sport)

    return result



# use nmap to scan network
# nmap -sP
def nmap_scan(ip):

    pass


if __name__ == '__main__':
    #  test arp_scan function  192.168.111.32
    print('test arp_scan function')
    result = arp_scan('192.168.103.255/24')
    for mapping in result:
        print('{} ==> {}'.format(mapping['IP'], mapping['MAC']))

    # test tcp_scan function
    print('test tcp_scan function',len(result))