import socket, traceback, select, pickle
import network_config as nc
import hub_message_handler as hmh

def initialise_socket():
    port = nc.get_port()
    ip_address = nc.get_ip()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # setup reusable address
    server_socket.bind((ip_address, port))
    server_socket.listen()
    return server_socket

def handle_read_sockets(read_sockets, server_socket, sockets_list, clients):
    for notified_socket in read_sockets:
        sockets_list, clients = handle_read_socket(notified_socket, server_socket, sockets_list, clients)
        return sockets_list, clients

def handle_read_socket(notified_socket, server_socket, sockets_list, clients):
        if notified_socket == server_socket:
            sockets_list, clients = handle_new_connection(sockets_list, server_socket, clients)
        else:
            sockets_list, clients = handle_message_received(notified_socket, sockets_list, clients)
        return sockets_list, clients

def handle_new_connection(sockets_list, server_socket, clients):
    client_socket, client_address = server_socket.accept()
    user = receive_message(client_socket)
    if user is not False:
        sockets_list.append(client_socket)
        clients[client_socket] = user
        username = user['data']
        print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{username}")
    return sockets_list, clients

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(header_length)
        # handle no data received
        if not len(message_header):
            return False
        # handle received data
        else:
            message_length = int(message_header.decode("utf-8").strip())
            data = client_socket.recv(message_length) #might need to handle for excessive length
            unpickled_data = pickle.loads(data)
            return {"header":message_header, "data": unpickled_data }
    except:
        return False

def handle_message_received(notified_socket, sockets_list, clients):
    message = receive_message(notified_socket)
    if message is False:
        print(f"Closed connection from {clients[notified_socket]['data']}")
        return remove_client_socket(notified_socket, sockets_list, clients)
    user = clients[notified_socket]
    print(f"Received message: {message['data']}")
    # send message to all other clients  ###BUSINESS LOGIC GOES HERE###
    for client_socket in clients:
        if client_socket != notified_socket:
            pickled_message_data = pickle.dumps(message['data'])
            message_header = f"{len(pickled_message_data) :< {header_length}}".encode('utf-8')
            client_socket.send(message_header + pickled_message_data)
    return sockets_list, clients

def handle_exception_sockets(read_sockets, server_socket, sockets_list, clients):
    for notified_socket in exception_sockets:
        sockets_list, clients = handle_exception_socket(exception_socket, server_socket, sockets_list, clients)
    return sockets_list, clients

def handle_exception_socket(exception_socket, server_socket, sockets_list, clients):
    return remove_client_socket(notified_socket, sockets_list, clients)

def remove_client_socket(notified_socket, sockets_list, clients):
    sockets_list.remove(notified_socket)
    del clients[notified_socket]
    return sockets_list, clients

server_socket = initialise_socket()
header_length = nc.get_header_length()
sockets_list = [server_socket]
clients = {}
while True:
    # get read, write and exception sockets
    read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)
    # handle read sockets
    sockets_list, clients = handle_read_sockets(read_sockets, server_socket, sockets_list, clients)
    # handle exception sockets
    sockets_list, clients = handle_exception_sockets(read_sockets, server_socket, sockets_list, clients)

