import hub_files.bad_socket_handler as bsh

def handle_exception_sockets(exception_sockets, sockets_list, clients):
    for notified_socket in exception_sockets:
        sockets_list, clients = handle_exception_socket(exception_socket, sockets_list, clients)
    return sockets_list, clients

def handle_exception_socket(exception_socket, sockets_list, clients):
    return bsh.remove_client_socket(exception_socket, sockets_list, clients)
