import socket, select
import network_config as nc
import hub_read_socket_handler as rsh
import hub_exception_socket_handler as esh

port = nc.get_port()
ip_address = nc.get_ip()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # setup reusable address
server_socket.bind((ip_address, port))
server_socket.listen()
header_length = nc.get_header_length()
sockets_list = [server_socket]
clients = {}
while True:
    read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)
    sockets_list, clients = rsh.handle_read_sockets(read_sockets, server_socket, sockets_list, clients)
    sockets_list, clients = esh.handle_exception_sockets(exception_sockets, sockets_list, clients)
