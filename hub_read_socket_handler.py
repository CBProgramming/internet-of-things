import socket, time, errno, pickle
import network_config as nc
import bad_socket_handler as bsh
import hub_message_handler as hmh
import network_pickler as np

def handle_read_sockets(read_sockets, server_socket, sockets_list, clients, mqtt_manager):
    for notified_socket in read_sockets:
        sockets_list, clients = handle_read_socket(notified_socket, server_socket, sockets_list, clients, mqtt_manager)
        return sockets_list, clients

def handle_read_socket(notified_socket, server_socket, sockets_list, clients, mqtt_manager):
    if notified_socket == server_socket:
        sockets_list, clients = handle_new_connection(sockets_list, server_socket, clients)
    else:
        sockets_list, clients = handle_message_received(notified_socket, sockets_list, clients, mqtt_manager)
    return sockets_list, clients

def handle_new_connection(sockets_list, server_socket, clients):
    client_socket, client_address = server_socket.accept()
    user = receive_message(client_socket)
    if user[0] == 'OK':
        sockets_list.append(client_socket)
        clients[client_socket] = user[1]
        print(f"Accepted new connection from username:{user[1]}")
    return sockets_list, clients

def handle_message_received(notified_socket, sockets_list, clients, mqtt_manager):
    message = receive_message(notified_socket)
    if not message or message[0] == 'ERROR':
        print(f"Closed connection from {clients[notified_socket]}")
        return bsh.remove_client_socket(notified_socket, sockets_list, clients)
    elif message[0] != 'NO_MESSAGES':
        sender = clients[notified_socket]
        hmh.handle_network_message(clients, notified_socket, message[1], mqtt_manager)
    return sockets_list, clients

def receive_message(client_socket):
    message = np.unpickle_message(client_socket)
    if message:
        return message
    else:
        return False
