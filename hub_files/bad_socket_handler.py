class BadSocketHandler:

    def __init__(self, sockets, clients, rhm):
        self.sockets = sockets
        self.clients = clients
        self.rhm = rhm
        
    def remove_client_socket(self, notified_socket):
        if self.clients[notified_socket] == 'remote_hub':
            self.rhm.current_state = 'OK'
        self.sockets.remove(notified_socket)
        del self.clients[notified_socket]
