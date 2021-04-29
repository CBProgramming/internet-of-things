import time, network_management.socket_manager
import subprocess
import socket

username = "remote_hub_actuator"
remote_hub_script = 'remote_hub.py'
remote_on = False


# register socket with transport layer
while True:
    time.sleep(1)
    sm = network_management.socket_manager.SocketManager()
    status = 'OFFLINE'
    while status == 'OFFLINE':
        #print("Attempting to register")
        status = sm.connect(username)
        #print(status)
        if status == 'OFFLINE':  ## sm tries five times on both hubs
                                 ## before returning an 'OFFLINE' result
            print("Registration attempt failed")
            time.sleep(1)
            # this might need better handling as currently it just
            # spams the network every second
            # probably want to wait an incrementing amount of time before
            # trying sm.connect again
    #print("While over")
    #messaging loop
    inner_while = True
    while inner_while:
        # receive result, which is a list in the format [result_code, message]
        result = sm.receive_message()
        #print(result)
        if result:
            result_code = result[0]
            #if result_code != 'ERROR':
                #print("Result code: " + str(result_code))
            # result code 'OK' indicates a message was successfully received
            if result_code == 'OK':
                message = result[1]
                #print(message)
                if message == 'ON' and not remote_on:
                    try:
                        print("Going out of range of home hub...")
                        print("Turning on remote hub...")
                        remote_hub_process = subprocess.Popen(['python','remote_hub.py'])
                        remote_on = True
                    except Exception as e:
                        print("Exception when turning on remote hub: " + str(e))
                elif message == 'OFF':
                    try:
                        print("Pet has returned home")
                        print("Switching off remote hub...")
                        remote_hub_process.terminate()
                        remote_on = False
                        inner_while = False
                    except Exception as e:
                        print("Exception when turning off remote hub: " + str(e))
            if result_code == 'SOCKET_EXCEPTION':
                inner_while = False
        else:
            #print("Result == None")
            #print(result)
            inner_while = False
    if sm.socket:
        #print("Closing socket")
        sm.socket.shutdown(socket.SHUT_RDWR)
            # Other result codes you might want to handle for:
            # 'INVALID_HEADER'  (This would indicate there is something wrong with the
            #                    network_config or socket_manager scripts)
            # 'NO_MESSAGES'  (This is an error you'll get whenever there's no messages
            #                 and it probably doesn't need handling as long as your
            #                 receive loop keeps running)
            # 'SOCKET_EXCEPTION' (This is if something inexplicably goes wrong)
