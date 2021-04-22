import socket, pickle
import network_config as nc

def handle_message(sockets_list, clients, notified_socket, message):
    user = clients[notified_socket]
    print(f"Received message: {message['data']}")
    # send message to all other clients  ###BUSINESS LOGIC GOES HERE###
    for client_socket in clients:
        if client_socket != notified_socket:
            header_length = nc.get_header_length()
            pickled_message_data = pickle.dumps(message['data'])
            message_header = f"{len(pickled_message_data) :< {header_length}}".encode('utf-8')
            client_socket.send(message_header + pickled_message_data)
    return sockets_list, clients
