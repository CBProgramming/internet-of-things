import time
import network_config as nc
import socket_manager as sm

username = "Mock Sensor 2"
client_socket = sm.get_socket()

# register socket with transport layer
registered = False
while not registered:
    registered = sm.register(username, client_socket)
    if not registered:
        print("Registration attempt failed")
        time.sleep(1) # this might need better handling as currently it just
                      # spams the network every second
   
#messaging loop
count = 200
while True:
    time.sleep(1) # don't do this on real code (unless its relevant to simulating data)

    # set up dummy message
    message = (f"{username} > Message number: " + str(count))
    count = count + 1

    # attempt to send message, variable 'success' stores a boolean
    # value indicating if message sending was successful
    success = sm.send_message(client_socket, message)
    
