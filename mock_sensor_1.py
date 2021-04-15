import os
import network_config as nc
import socket
import select
import time
import errno # error code matcher

my_username = "Mock Sensor 1"
port = nc.get_port()
ip_address = nc.get_ip()
#ip_address = '192.168.0.5'
header_length = nc.get_header_length()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((ip_address, port))
client_socket.setblocking(False)

#register with the server
username = my_username.encode('utf-8')
username_header = f"{len(username):<{header_length}}".encode('utf-8')
print(len(username_header))
client_socket.send(username_header + username)

count = 1

#messaging loop
while True:
    time.sleep(1)
    message = (f"{my_username} > Message number: " + str(count))
    count = count + 1
    #if theres a message
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message) :< {header_length}}".encode('utf-8')
        client_socket.send(message_header + message)
    try:
        #receive messages
        while True:
            username_header = client_socket.recv(header_length)
            #if no data
            if not len(username_header):
                print("Connection cliosed by the server")
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(header_length)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")
    #once there are no messages to receive an error will break the inner while loop
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Error', str(e))
            continue # continues outer loop
    except Exception as e:
        
        print('General error',str(e))
        sys.exit()
