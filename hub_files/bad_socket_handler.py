class BadSocketHandler:

    def __init__(self, sockets, clients, rhm):
        self.sockets = sockets
        self.clients = clients
        self.rhm = rhm
        
    def remove_client_socket(self, notified_socket):
        #print("BSH: remove_client_socket")
        #print(notified_socket)
        try:
            if self.clients[notified_socket] == 'remote_hub':
                self.rhm.current_state = 'OK'
        except:
            None
        try:
            self.sockets.remove(notified_socket)
        except:
            None
        try:
            del self.clients[notified_socket]
        except:
            None
        
        
