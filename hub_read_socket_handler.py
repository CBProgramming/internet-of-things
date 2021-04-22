import socket, time, errno, pickle
import network_config as nc
import bad_socket_handler as bsh
import hub_message_handler as hmh

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
        header_length = nc.get_header_length()
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
    except Exception as e:
        print("Read socket handler exception: " + str(e))
        return False

def handle_message_received(notified_socket, sockets_list, clients):
    message = receive_message(notified_socket)
    if message is False:
        print(f"Closed connection from {clients[notified_socket]['data']}")
        return bsh.remove_client_socket(notified_socket, sockets_list, clients)
    else:
        sockets_list, clients = hmh.handle_message(sockets_list, clients, notified_socket, message)
    return sockets_list, clients
