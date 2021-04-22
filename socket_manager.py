import socket, time, errno, pickle
import network_config as nc

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
        username_pickle = pickle.dumps(username)
        header_length = nc.get_header_length()
        username_header = f"{len(username_pickle):<{header_length}}".encode('utf-8')
        client_socket.sendall(username_header + username_pickle)
        return True
    except:
        return False


def send_message(client_socket, message):
    try:
        if message:
            message_pickle = pickle.dumps(message)
            header_length = nc.get_header_length()
            message_header = f"{len(message_pickle) :< {header_length}}".encode('utf-8')
            client_socket.send(message_header + message_pickle)
            return True
        else:
            print("No message")
            return False
    except Exception as e:
        print("Send message exception: " + str(e))
        return False

def receive_message(client_socket):
    try:
        header_length = nc.get_header_length()
        while True:
            message_header = client_socket.recv(header_length)
            if not len(message_header):
                return [invalid_header, empty_string]
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length)
            unpickled_message = pickle.loads(message)
            return [ok_result, unpickled_message]
    #once there are no messages to receive an error will break the inner while loop
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            return [no_messages, str(e)]
        return [no_messages, str(e)]
    except Exception as e:
        return [error, e]
        
