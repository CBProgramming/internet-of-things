import socket
import network_pickler as np

def handle_message(sockets_list, clients, notified_socket, message, sender):
    print("Handle message: ")
    print(message)
    try:
        user = clients[notified_socket]
        print(f"Received message: {message}")
        # send message to all other clients  ###BUSINESS LOGIC GOES HERE###
        # variable sender contains username to determine course of action
        for client_socket in clients:
            if client_socket != notified_socket:
                pickled_message = np.pickle_message(message)
                client_socket.send(pickled_message)
    except Exception as e:
        print("Hub message handler error: " + str(e))
