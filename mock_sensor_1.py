import time
import network_management.socket_manager

username = "Mock Sensor 1"
sm = network_management.socket_manager.SocketManager()

# register socket with transport layer
status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = sm.connect(username)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
                             ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)
        # this might need better handling as currently it just
        # spams the network every second
        # probably want to wait an incrementing amount of time before
        # trying sm.connect again

#messaging loop
count = 100
while True:
    time.sleep(1) # don't do this on real code (unless its relevant to simulating data)
    
    # set up dummy message
    message = (f"Message number: " + str(count))
    #message = [1, 'string', ['list', 0]]
    print("Sending message: " + str(message))
    count = count + 1
    
    # attempt to send message, variable 'success' stores a boolean
    # value indicating if message sending was successful
    result = sm.send_message(message)

    #POSSIBLE RESULTS
    # 'OK'
    # 'INVALID MESSAGE FORMAT'
    # 'OFFLINE'    This one means 5 recconect attempts were tried on both hubs
