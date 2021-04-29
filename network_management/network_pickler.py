import pickle, errno
import network_management.network_config as nc

def pickle_message(message):
    message_pickle = pickle.dumps(message)
    header_length = nc.get_header_length()
    message_header = f"{len(message_pickle):<{header_length}}".encode('utf-8')
    pickled_message = message_header + message_pickle
    return pickled_message

def unpickle_message(client_socket):
    try:
        header_length = nc.get_header_length()
        message_header = client_socket.recv(header_length)
        # handle no data received
        if not len(message_header):
            return ['INVALID_HEADER','']
        # handle received data
        else:
            message_length = int(message_header.decode("utf-8").strip())
            data = client_socket.recv(message_length) #might need to handle for excessive length
            unpickled_data = pickle.loads(data)
            return ['OK',unpickled_data]
    except Exception as e:
        return ['ERROR',str(e)]
        
