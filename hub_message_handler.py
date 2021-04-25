import socket, json
import network_pickler as np

class HubMessageHandler():

    def __init__(self, clients, mqtt_manager):
        self.clients = clients
        self.mqtt_manager = mqtt_manager
        self.mqtt_manager.hmh = self

    def handle_network_message(self, notified_socket, message):
        try:
            sensor = self.clients[notified_socket]
            self.mqtt_manager.publish_message(sensor, json.dumps(message))
        except Exception as e:
            print("Hub message publish error: " + str(e))

    def handle_mqtt_message(self, message):
        message_key = message[0]
        data = message[1]
        for key, value in self.clients.items():
            if message_key == value:
                pickled_message = np.pickle_message(data)
                key.send(pickled_message)

    def send_to_all(self, notified_socket, message):
        for client_socket in self.clients:
            if client_socket != notified_socket:
                pickled_message = np.pickle_message(message)
                client_socket.send(pickled_message)
    
