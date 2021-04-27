import socket

port = 8301
remote_port = 8302
header_length = 10

def get_port():
    return port

def get_header_length():
    return header_length

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.255.255.255', 1))
    ip_address = s.getsockname()[0]
    return ip_address
    
