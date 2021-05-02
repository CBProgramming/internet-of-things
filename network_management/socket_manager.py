import socket, errno, time
import network_management.network_config as nc
import network_management.network_pickler as np

empty_string = ''
invalid_header = 'INVALID_HEADER'
ok_result = 'OK'
no_messages = 'NO_MESSAGES'
error = 'ERROR'
nb_error = '[WinError 10035] A non-blocking socket operation could not be completed immediately'

class SocketManager:
    def __init__(self):
        #print("SM: __init__ socket manager starts")
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
        #print("SM: connect starts")
        self.username = username
        attempts = 0
        while attempts < self.connect_attempts:
            self.socket = self.get_socket()
            success = self.register()
            if success:
                print("Connected to home hub")
            if not success:
                self.socket = self.get_remote_socket()
                success = self.register()
                if success:
                    print("Connected to remote hub")
            if success:
                return self.online
            else:
                attempts = attempts + 1
        return self.offline

    def initialise_socket(self, port):
        #print("SM: initialise socket starts")
        ip_address = nc.get_ip()
        header_length = nc.get_header_length()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.connect((ip_address, port))
        client_socket.setblocking(False)
        return client_socket

    def get_socket(self):
        #print("SM: get socket starts")
        port = nc.get_port()
        return self.initialise_socket(port)

    def get_remote_socket(self):
        #print("SM: get remote socket starts")
        port = nc.get_remote_port()
        return self.initialise_socket(port)

    def register(self):
        #print("SM: register starts")
        try:
            pickled_message = np.pickle_message(self.username)
            bytes_sent = self.socket.send(pickled_message)
            time.sleep(0.4)
            response = self.internal_receive_message()
            #print(response)
            if response[0] == 'OK' and response[1] == 'welcome':
                #print("Successfully registered with server")
                return True
            else:
                #print("Unable to connect to the server")
                return False
        except Exception as e:
            print("Socket manager registration exception: " + str(e))
            return False

    def internal_send_message(self, message):
        #print("SM: internal send message starts")
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
        #print("SM: send messaage starts")
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
        #print("SM: internal receive message starts")
        try:
            result =  np.unpickle_message(self.socket)
            if result:
                code = result[0]
                message = result[1]
                #if code != error and message != nb_error:
                    #if code == invalid_header: 
                        #print("SM: unpickle result:")
                        #print(result)
                        #print("Result printed")
            return result
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                return [no_messages, str(e)]
            return [no_messages, str(e)]
        except Exception as e:
            print("Socket manager receive message exception: " + str(e))
            return [self.socket_exception, e]
                
    def receive_message(self):
        #print("SM: receive message starts")
        attempts = 0
        while attempts < self.receive_message_attempts:
            result_list = self.internal_receive_message()
            result = result_list[0]
            #print(result)
            if result == self.ok_result or result == self.no_messages or result == self.error:
                #print("Returning: ")
                #print(result_list)
                return result_list
            if result == self.socket_exception or result == self.invalid_header:
                #status = self.connect(self.username)
                if status == self.offline:
                    #print("Returning: ")
                    #print(result_list)
                    return result_list
                    
            attempts = attempts + 1
        #print("Nothing to return")
        
