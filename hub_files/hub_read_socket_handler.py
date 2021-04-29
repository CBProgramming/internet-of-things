import socket
import hub_files.bad_socket_handler
import hub_files.hub_message_handler
import network_management.network_pickler as np
import hub_files.mqtt_manager
import hub_files.remote_hub_monitor
import hub_files.gps_range_calculator as grc
import mock_config.default_variables as dv

class ReadSocketHandler:
    def __init__ (self, server_socket):
        self.in_range = True
        self.clients = {}
        self.server_socket = server_socket
        self.sockets = [server_socket]
        self.mqtt_manager = hub_files.mqtt_manager.MqttManager()
        self.rhm = hub_files.remote_hub_monitor.RemoteHubMonitor(self.clients, self.mqtt_manager)
        self.bsh = hub_files.bad_socket_handler.BadSocketHandler(self.sockets, self.clients, self.rhm)
        self.hmh = hub_files.hub_message_handler.HubMessageHandler(self.clients, self.mqtt_manager)
        
        
    def handle_read_sockets(self, read_sockets):
        #print("Preparing to handle read sockets")
        for notified_socket in read_sockets:
            self.handle_read_socket(notified_socket)
        #print("Preparing to manage MQTT queue")
        self.mqtt_manager.manage_queued_messages()

    def handle_read_socket(self, notified_socket):
        if notified_socket == self.server_socket:
            self.handle_new_connection()
        else:
            self.handle_message_received(notified_socket)

    def handle_new_connection(self):
        if self.in_range:
            client_socket, client_address = self.server_socket.accept()
            user = self.receive_message(client_socket)
            if user[0] == 'OK':
                self.sockets.append(client_socket)
                self.clients[client_socket] = user[1]
                print(f"Accepted new connection from device: {user[1]}")

    def handle_message_received(self, notified_socket):
        message = self.receive_message(notified_socket)
        if not message or message[0] == 'ERROR':
            print(f"Closed connection from device: {self.clients[notified_socket]}")
            self.bsh.remove_client_socket(notified_socket)
        elif message[0] != 'NO_MESSAGES':
            sender = self.clients[notified_socket]
            self.hmh.handle_network_message(notified_socket, message[1])
            if sender == 'gps_sensor':
                collar_range = grc.translate_gps(message[1])
                print("Collar range = " + str(collar_range))
                if collar_range == 'EXCEEDED RANGE':
                    self.in_range = False
                    self.remove_ranged_devices()

    def remove_ranged_devices(self):
        print("Removing ranged devices")
        sockets_to_remove = []
        for username in dv.ranged_devices:
            for key, value in self.clients.items():
                #print("Key:")
                #print(key)
                #print("Value:")
                #print(value)
                if username == value:
                    sockets_to_remove.append(key)
        for socket in sockets_to_remove:
            self.sockets.remove(socket)
            del self.clients[socket]
        sockets_to_remove = None
        print("Finished removing ranged devices")

    def receive_message(self, client_socket):
        message = np.unpickle_message(client_socket)
        if message:
            return message
        else:
            return False
