import time
import network_management.socket_manager

username = "Mock Actuator 1"
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
while True:
    #print("Attempting to receive message")
    # receive result, which is a list in the format [result_code, message]
    result = sm.receive_message()
    #print("Message received: " + str(result))
    result_code = result[0]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        print(message)

    # Other result codes you might want to handle for:
    # 'INVALID_HEADER'  (This would indicate there is something wrong with the
    #                    network_config or socket_manager scripts)
    # 'NO_MESSAGES'  (This is an error you'll get whenever there's no messages
    #                 and it probably doesn't need handling as long as your
    #                 receive loop keeps running)
    # 'SOCKET_EXCEPTION' (This is if something inexplicably goes wrong)
