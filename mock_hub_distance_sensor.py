import time
import network_management.socket_manager as sm

username = "range_sensor"
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
count = 1
while True:
    time.sleep(1) # don't do this on real code (unless its relevant to simulating data)
    
    # set up dummy message
    if count < 5:
        message = ("OK")
    elif count < 15:
        message = ("AT BOUNDARY")
    elif count < 25:
        client_socket = None
        registered = False
    elif count < 35:
        if client_socket == None:
            client_socket = sm.get_socket()
            while not registered:
                registered = sm.register(username, client_socket)
                if not registered:
                    print("Registration attempt failed")
                    time.sleep(1)
        message = ("AT BOUNDARY")
    else:
        message = ("OK")
    #message = [1, 'string', ['list', 0]]
    print("Sending message: " + str(message))
    count = count + 1
    # attempt to send message, variable 'success' stores a boolean
    # value indicating if message sending was successful
    success = sm.send_message(client_socket, message)