import socket, errno
import network_management.network_config as nc
import network_management.network_pickler as np

empty_string = ''
invalid_header = 'INVALID_HEADER'
ok_result = 'OK'
no_messages = 'NO_MESSAGES'
error = 'ERROR'

def get_socket():
    port = nc.get_port()
    ip_address = nc.get_ip()
    header_length = nc.get_header_length()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port))
    client_socket.setblocking(False)
    return client_socket

def register(username, client_socket):
    try:
        pickled_message = np.pickle_message(username)
        client_socket.send(pickled_message)
        return True
    except Exception as e:
        print("Socket manager registration exception: " + str(e))
        return False


def send_message(client_socket, message):
    try:
        if message:
            pickled_message = np.pickle_message(message)
            client_socket.send(pickled_message)
            return True
        else:
            print("An attempt was made to send an empty message")
            return False
    except Exception as e:
        print("Socket manager send message exception: " + str(e))
        return False

def receive_message(client_socket):
    try:
        return np.unpickle_message(client_socket)
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            return [no_messages, str(e)]
        return [no_messages, str(e)]
    except Exception as e:
        print("Socket manager receive message exception: " + str(e))
        return [error, e]
