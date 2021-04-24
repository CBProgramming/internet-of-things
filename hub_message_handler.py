import socket, json
import network_pickler as np

def handle_network_message(clients, notified_socket, message, mqtt_manager):
    try:
        sensor = clients[notified_socket]
        mqtt_manager.publish_message(sensor, json.dumps(message))
    except Exception as e:
        print("Hub message publish error: " + str(e))

def handle_mqtt_message(network_clients, message):
    message_key = message[0]
    data = message[1]
    for key, value in network_clients.items():
        if message_key == value:
            pickled_message = np.pickle_message(data)
            key.send(pickled_message)

def send_to_all(clients, notified_socket, message, mqtt_manager):
    for client_socket in clients:
        if client_socket != notified_socket:
            pickled_message = np.pickle_message(message)
            client_socket.send(pickled_message)
    
