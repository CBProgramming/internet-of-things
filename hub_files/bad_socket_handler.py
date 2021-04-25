class BadSocketHandler:

    def __init__(self, sockets, clients):
        self.sockets = sockets
        self.clients = clients
        
    def remove_client_socket(self, notified_socket):
        self.sockets.remove(notified_socket)
        del self.clients[notified_socket]
