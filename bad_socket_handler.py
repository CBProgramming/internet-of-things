def remove_client_socket(notified_socket, sockets_list, clients):
    sockets_list.remove(notified_socket)
    del clients[notified_socket]
    return sockets_list, clients
