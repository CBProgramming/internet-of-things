import socket
import network_pickler as np

def handle_network_message(sockets_list, clients, notified_socket, message, sender):
    #print("Handle message: ")
    #print("Sockets list: " + str(sockets_list))
    #print("Clients: " + str(clients))
    #print(message)
    try:
        user = clients[notified_socket]
        #print("User")
        #print(user)
        print(f"Received message: {message}")
        # send message to all other clients  ###BUSINESS LOGIC GOES HERE###
        # variable sender contains username to determine course of action
        for client_socket in clients:
            if client_socket != notified_socket:
                pickled_message = np.pickle_message(message)
                client_socket.send(pickled_message)
    except Exception as e:
        print("Hub message handler error: " + str(e))

def handle_mqtt_message(network_clients, message, mqtt_client):
    print("Handle mqqt message called")
    print(message)
    message_key = message[0]
    data = message[1]
    for key, value in network_clients.items():
        if message_key == value:
            pickled_message = np.pickle_message(data)
            key.send(pickled_message)
    
