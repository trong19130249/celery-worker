import socket


def get_ipv4_address():
    """
    Get the IPv4 address of the device.

    Returns:
        str: The IPv4 address of the device.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipV4= s.getsockname()[0]
    s.close()
    return ipV4