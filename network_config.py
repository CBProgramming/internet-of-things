import socket

port = 8301
header_length = 10

def get_port():
    return port

def get_header_length():
    return header_length

def get_ip():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return ip_address
    
