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
        status = sm.connect(username)
        if status == 'OFFLINE':
            print("Registration attempt failed")
            time.sleep(1)

    inner_while = True
    while inner_while:
        result = sm.receive_message()
        if result:
            result_code = result[0]
            if result_code == 'OK':
                message = result[1]
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
            inner_while = False
    if sm.socket:
        sm.socket.shutdown(socket.SHUT_RDWR)
