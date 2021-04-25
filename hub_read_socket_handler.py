import socket
import bad_socket_handler
import hub_message_handler as hmh
import network_pickler as np

class ReadSocketHandler:
    def __init__ (self, _mqtt_manager, server_socket):
        self.mqtt_manager = _mqtt_manager
        self.clients = {}
        self.server_socket = server_socket
        self.sockets = [server_socket]
        self.bsh = bad_socket_handler.BadSocketHandler(self.sockets, self.clients)
        
    def handle_read_sockets(self, read_sockets):
        for notified_socket in read_sockets:
            self.handle_read_socket(notified_socket)
        self.clients = self.mqtt_manager.manage_queued_messages(self.clients)

    def handle_read_socket(self, notified_socket):
        if notified_socket == self.server_socket:
            self.handle_new_connection()
        else:
            self.handle_message_received(notified_socket, self.mqtt_manager)

    def handle_new_connection(self):
        client_socket, client_address = self.server_socket.accept()
        user = self.receive_message(client_socket)
        if user[0] == 'OK':
            self.sockets.append(client_socket)
            self.clients[client_socket] = user[1]
            print(f"Accepted new connection from device: {user[1]}")

    def handle_message_received(self, notified_socket, mqtt_manager):
        message = self.receive_message(notified_socket)
        if not message or message[0] == 'ERROR':
            print(f"Closed connection from device: {self.clients[notified_socket]}")
            self.bsh.remove_client_socket(notified_socket)
        elif message[0] != 'NO_MESSAGES':
            sender = self.clients[notified_socket]
            hmh.handle_network_message(self.clients, notified_socket, message[1], mqtt_manager)

    def receive_message(self, client_socket):
        message = np.unpickle_message(client_socket)
        if message:
            return message
        else:
            return False
