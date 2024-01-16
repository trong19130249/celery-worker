# scan network for devices and print their ip addresses and mac addresses and metadata
# input: network address  192.168.103.11/24

import argparse
from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether, ARP
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)
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

def long2net(arg):
    if (arg <= 0 or arg >= 0xFFFFFFFF):
        raise ValueError("illegal netmask value", hex(arg))
    return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))

def to_CIDR_notation(bytes_network, bytes_netmask):
    network = scapy.utils.ltoa(bytes_network)
    netmask = long2net(bytes_netmask)
    net = "%s/%s" % (network, netmask)
    if netmask < 16:
        logger.warning("%s is too big. skipping" % net)
        return None
    return net




# def scan_neighbourhood():
#     # Get the IPv4 address of the device
#     ip_address = get_ipv4_address()


#     # Perform ARP scan
#     result = arp_scan(ip_address + '/24')
#     # Print IP addresses and MAC addresses
#     for mapping in result:
#         print('{} ==> {}'.format(mapping['IP'], mapping['MAC']))

def scan_neighbourhood(interface_to_scan=None):
    if os.geteuid() != 0:
        print('You need to be root to run this script', file=sys.stderr)
        sys.exit(1)
    results = []  # Create an empty list to store the results
    for network, netmask, _, interface, address, _ in scapy.config.conf.route.routes:
        if interface_to_scan and interface_to_scan != interface:
            continue
        if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
            continue
        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue
        if interface != interface_to_scan \
                and (interface.startswith('docker')
                     or interface.startswith('br-')
                     or interface.startswith('tun')):
            print("Skipping interface '%s'" % interface)
            continue
        net = to_CIDR_notation(network, netmask)
        if net:
            results.extend(arp_scan(net))  # Append the results of arp_scan to the list
    return results  # Return the list of results

if __name__ == '__main__':
    results = scan_neighbourhood()
    # Print IP addresses and MAC addresses
    for mapping in results:
        print('{} ==> {}'.format(mapping['IP'], mapping['MAC']))
            