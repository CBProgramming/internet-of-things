import socket
import hub_files.bad_socket_handler
import hub_files.hub_message_handler
import network_management.network_pickler as np
import hub_files.mqtt_manager
import hub_files.remote_hub_monitor
import hub_files.gps_range_calculator as grc
import mock_config.default_variables as dv

class ReadSocketHandler:
    def __init__ (self, server_socket, hub_type):
        self.hub_type = hub_type
        self.in_range = True
        if hub_type == 'remote':
            self.in_range = False
        self.clients = {}
        self.server_socket = server_socket
        self.sockets = [server_socket]
        self.mqtt_manager = hub_files.mqtt_manager.MqttManager()
        self.rhm = hub_files.remote_hub_monitor.RemoteHubMonitor(self.clients, self.mqtt_manager)
        self.bsh = hub_files.bad_socket_handler.BadSocketHandler(self.sockets, self.clients, self.rhm)
        self.hmh = hub_files.hub_message_handler.HubMessageHandler(self.clients, self.mqtt_manager, self)
        
        
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
        if self.in_range or self.hub_type == 'remote':
            client_socket, client_address = self.server_socket.accept()
            user = self.receive_message(client_socket)
            if user[0] == 'OK':
                pickled_message = np.pickle_message('welcome')
                client_socket.send(pickled_message)
                self.sockets.append(client_socket)
                self.clients[client_socket] = user[1]
                print(f"Accepted new connection from device: {user[1]}")
        else:
            #print("New connection attempted but out of range")
            None

    def handle_message_received(self, notified_socket):
        message = self.receive_message(notified_socket)
        if not message or message[0] == 'ERROR':
            print(f"HRH: Closed connection from device: {self.clients[notified_socket]}")
            notified_socket.shutdown(socket.SHUT_RDWR)
            self.bsh.remove_client_socket(notified_socket)
        elif message[0] != 'NO_MESSAGES':
            sender = self.clients[notified_socket]
            #print("Message: " + str(message[1]))
            if message[1] == "let me in":
                #print("Permission requested")
                None
            else:
                self.hmh.handle_network_message(notified_socket, message[1])
            if sender == 'gps_sensor':
                collar_range = grc.translate_gps(message[1])
                #print("Collar range = " + str(collar_range))
                if self.hub_type == 'home':
                    if collar_range == "AT BOUNDARY":
                        self.hmh.handle_mqtt_message(['remote_hub_actuator','ON'])
                    if collar_range == 'EXCEEDED RANGE':
                        if self.in_range:
                            print("Pet no longer in range of home hub")
                        self.in_range = False
                        self.remove_ranged_devices()
                elif self.hub_type == 'remote':
                    if collar_range == "OK":
                        self.hmh.handle_mqtt_message(['remote_hub_actuator','OFF'])


    def remove_ranged_devices(self):
        #print("Removing ranged devices")
        sockets_to_remove = []
        for username in dv.ranged_devices:
            for key, value in self.clients.items():
                if username == value:
                    sockets_to_remove.append(key)
        for _socket in sockets_to_remove:
            self.sockets.remove(_socket)
            del self.clients[_socket]
            _socket.shutdown(socket.SHUT_RDWR)
        sockets_to_remove = None
        #print("Finished removing ranged devices")

    def receive_message(self, client_socket):
        message = np.unpickle_message(client_socket)
        if message:
            return message
        else:
            return False
