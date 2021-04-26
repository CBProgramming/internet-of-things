import socket, json
import network_management.network_pickler as np
import hub_files.remote_hub_monitor

class HubMessageHandler():

    def __init__(self, clients, mqtt_manager):
        self.clients = clients
        self.mqtt_manager = mqtt_manager
        self.mqtt_manager.hmh = self
        self.rhm = hub_files.remote_hub_monitor.RemoteHubMonitor(self.clients, self.mqtt_manager)

    def handle_network_message(self, notified_socket, message):
        try:
            sensor = self.clients[notified_socket]
            self.mqtt_manager.publish_message(sensor, json.dumps(message))
        except Exception as e:
            print("Hub message publish error: " + str(e))
        device = self.clients[notified_socket]
        if device == 'range_sensor':
            self.rhm.determine_network_health(message)
            

    def handle_mqtt_message(self, message):
        #print("HUB_MESSAGE_HANDLER - MQTT message received: " + str(message[1]))
        message_key = message[0]
        data = message[1]
        for key, value in self.clients.items():
            if message_key == value:
                pickled_message = np.pickle_message(data)
                key.send(pickled_message)
        #print("Finished handling MQTT messages")

    def send_to_all(self, notified_socket, message):
        for client_socket in self.clients:
            if client_socket != notified_socket:
                pickled_message = np.pickle_message(message)
                client_socket.send(pickled_message)
    
