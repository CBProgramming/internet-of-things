import socket, errno
import network_management.network_config as nc
import network_management.network_pickler as np

empty_string = ''
invalid_header = 'INVALID_HEADER'
ok_result = 'OK'
no_messages = 'NO_MESSAGES'
error = 'ERROR'

class SocketManager:
    def __init__(self):
        self.empty_string = ''
        self.invalid_header = 'INVALID_HEADER'
        self.invalid_message = 'INVALID MESSAGE'
        self.ok_result = 'OK'
        self.no_messages = 'NO_MESSAGES'
        self.error = 'ERROR'
        self.socket_exception = 'SOCKET_EXCEPTION'
        self.online = 'ONLINE'
        self.offline = 'OFFLINE'
        self.username = ''
        self.connect_attempts = 5
        self.send_message_attempts = 3
        self.receive_message_attempts = 3

    def connect(self, username):
        self.username = username
        attempts = 0
        while attempts < self.connect_attempts:
            self.socket = self.get_socket()
            success = self.register()
            if not success:
                self.socket = self.get_remote_socket()
                success = self.register()
            if success:
                return self.online
            else:
                attempts = attempts + 1
        return self.offline

    def initialise_socket(self, port):
        ip_address = nc.get_ip()
        header_length = nc.get_header_length()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port))
        client_socket.setblocking(False)
        return client_socket

    def get_socket(self):
        port = nc.get_port()
        return self.initialise_socket(port)

    def get_remote_socket(self):
        port = nc.get_remote_port()
        return self.initialise_socket(port)

    def register(self):
        try:
            pickled_message = np.pickle_message(self.username)
            self.socket.send(pickled_message)
            return True
        except Exception as e:
            print("Socket manager registration exception: " + str(e))
            return False

    def internal_send_message(self, message):
        try:
            if message:
                pickled_message = np.pickle_message(message)
                self.socket.send(pickled_message)
                return self.ok_result
            else:
                print("An attempt was made to send an empty message")
                return self.invalid_message
        except Exception as e:
            print("Socket manager send message exception: " + str(e))
            return self.socket_exception

    def send_message(self, message):
        attempts = 0
        while attempts < self.send_message_attempts:
            result = self.internal_send_message(message)
            if result == self.ok_result or result == self.invalid_message:
                return result
            elif result == self.socket_exception:
                status = self.connect(self.username)
                if status == self.offline:
                    return status
            attempts = attempts + 1

    def internal_receive_message(self):
        try:
            return np.unpickle_message(self.socket)
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                return [no_messages, str(e)]
            return [no_messages, str(e)]
        except Exception as e:
            print("Socket manager receive message exception: " + str(e))
            return [self.socket_exception, e]
                
    def receive_message(self):
        attempts = 0
        while attempts < self.receive_message_attempts:
            result_list = self.internal_receive_message()
            result = result_list[0]
            #print(result)
            if result == self.ok_result or result == self.no_messages or result == self.error:
                #print("Returning: ")
                #print(result_list)
                return result_list
            if result == self.socket_exception:
                status = self.connect(self.username)
                if status == self.offline:
                    #print("Returning: ")
                    #print(result_list)
                    return result_list
                    
            attempts = attempts + 1
        #print("Nothing to return")
        
