import os, socket, select, time, errno, pickle
import network_config as nc

port = nc.get_port()
ip_address = nc.get_ip()
header_length = nc.get_header_length()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip_address, port))
client_socket.setblocking(False)

#register with the server
username = "Mock Sensor 1"
username_pickle = pickle.dumps(username)
username_header = f"{len(username_pickle):<{header_length}}".encode('utf-8')
client_socket.send(username_header + username_pickle)


#messaging loop
count = 1
while True:
    time.sleep(1)
    message = (f"{username} > Message number: " + str(count))
    count = count + 1
    #if there's data to send to transport layer (sensors)
    if message:
        message_pickle = pickle.dumps(message)
        message_header = f"{len(message_pickle) :< {header_length}}".encode('utf-8')
        client_socket.send(message_header + message_pickle)
    #if the device needs to check for received messages (actuators)
    try:
        #receive messages
        while True:
            message_header = client_socket.recv(header_length)
            #if header not as expected, close connection
            if not len(message_header):
                print("Connection closed")
                sys.exit() # maybe needs better handling that just stopping the script
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length)
            unpickled_message = pickle.loads(message)
            print(unpickled_message)
    #once there are no messages to receive an error will break the inner while loop
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Error', str(e))
            continue # continues outer loop
    except Exception as e:
        print('General error',str(e))
        sys.exit() # maybe needs better handling that just stopping the script
