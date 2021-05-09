import socket
import hub_files.bad_socket_handler
import hub_files.hub_message_handler
import network_management.network_pickler as np
import hub_files.mqtt_manager
import hub_files.remote_hub_monitor
import hub_files.gps_range_calculator as grc
import mock_config.default_variables as dv
import time
import datetime as dt

class ReadSocketHandler:
    def __init__ (self, server_socket, hub_type):
        self.hub_type = hub_type
        self.in_range = True
        self.at_home = True
        self.at_boundary = False
        self.beyond_boundary = False
        if hub_type == 'remote':
            self.in_range = False
        self.clients = {}
        self.old_clients = []
        self.new_clients = []
        self.current_clients = []
        self.previous_second = '61'
        self.print_connections = False
        self.server_socket = server_socket
        self.sockets = [server_socket]
        self.mqtt_manager = hub_files.mqtt_manager.MqttManager()
        self.rhm = hub_files.remote_hub_monitor.RemoteHubMonitor(self.clients, self.mqtt_manager)
        self.bsh = hub_files.bad_socket_handler.BadSocketHandler(self.sockets, self.clients, self.rhm)
        self.hmh = hub_files.hub_message_handler.HubMessageHandler(self.clients, self.mqtt_manager, self)
        
        
    def handle_read_sockets(self, read_sockets):
        current_second = dt.datetime.now().strftime("%S")
        if self.previous_second != current_second:
            #print("Second changed")
            self.previous_second = current_second
            self.print_connections = True
        #print("Preparing to handle read sockets")
        for notified_socket in read_sockets:
            self.handle_read_socket(notified_socket)
        #print("Preparing to manage MQTT queue")
        self.mqtt_manager.manage_queued_messages()
        if self.print_connections == True:
            self.print_connections = False
            self.print_connections_update()

    def get_current_clients(self):
        return list(self.clients.values())

    def print_connections_update(self):
        self.current_clients = self.get_current_clients()
        closed_connections = []
        new_connections = []
        for client in self.old_clients:
            if client not in self.current_clients:
                print("Closed connection from device: " + client)
        for client in self.current_clients:
            if client not in self.old_clients:
                print("Accepted new connection from device: " + client)
        self.old_clients = self.current_clients
        

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
                #print(f"Accepted new connection from device: {user[1]}")
        else:
            #print("New connection attempted but out of range")
            None

    def handle_message_received(self, notified_socket):
        message = self.receive_message(notified_socket)
        if not message or message[0] == 'ERROR':
            #print(f"HRH: Closed connection from device: {self.clients[notified_socket]}")
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
                    if collar_range == "OK":
                        self.at_home = True
                        self.at_boundary = False
                        if self.beyond_boundary:
                            self.beyond_boundary = False
                            self.mqtt_manager.publish_message("user_notification","PET_RETURNED")
                    if collar_range == "AT BOUNDARY":
                        self.at_boundary = True
                        if self.at_home:
                            self.at_home = False
                            self.beyond_boundary = False
                            self.mqtt_manager.publish_message("user_notification","BOUNDARY_REACHED")
                        elif self.beyond_boundary:
                            self.at_home = False
                            self.beyond_boundary = False
                            self.mqtt_manager.publish_message("user_notification","PET_RETURNED")
                        self.hmh.handle_mqtt_message(['remote_hub_actuator','ON'])
                    if collar_range == 'EXCEEDED RANGE':
                        self.beyond_boundary = True
                        if self.in_range:
                            if self.at_home or self.at_boundary:
                                self.at_home = False
                                self.at_boundary = False
                                self.mqtt_manager.publish_message("user_notification","PET_OUTSIDE_BOUNDARY")
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
