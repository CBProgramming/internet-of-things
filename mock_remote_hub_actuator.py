import time, network_management.socket_manager
import subprocess
import socket
from EmulatorGUI_controller import GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)

#username_feeder = "feeder_actuator"
username_remote_hub = "remote_hub_actuator"
username_camera = "camera_actuator"
username_microphone = "microphone_actuator"
username_speaker = "speaker_actuator"

remote_hub_script = 'remote_hub.py'
remote_on = False
online_status = 'ONLINE'
offline_status = 'OFFLINE'
reconnect_message = 'let me in'

remote_actuator_offline = True
camera_actuator_offline = True
microphone_actuator_offline = True
speaker_actuator_offline = True
remote_hub_socket = network_management.socket_manager.SocketManager()
camera_socket = network_management.socket_manager.SocketManager()
microphone_socket = network_management.socket_manager.SocketManager()
speaker_socket = network_management.socket_manager.SocketManager()

def flag_as_offline():
    remote_actuator_offline = True
    camera_actuator_offline = True
    microphone_actuator_offline = True
    speaker_actuator_offline = True

def reset_socket_managers():
    try:
        remote_hub_socket.socket.shutdown(socket.SHUT_RDWR)
    except:
        None
    remote_hub_socket = network_management.socket_manager.SocketManager()
    try:
        camera_socket.socket.shutdown(socket.SHUT_RDWR)
    except:
        None
    camera_socket = network_management.socket_manager.SocketManager()
    try:
        microphone_socket.socket.shutdown(socket.SHUT_RDWR)
    except:
        None
    microphone_socket = network_management.socket_manager.SocketManager()
    try:
        speaker_socket.socket.shutdown(socket.SHUT_RDWR)
    except:
        None
    speaker_socket = network_management.socket_manager.SocketManager()
    

# register socket with transport layer
while True:
    flag_as_offline()
    time.sleep(1)
    reset_socket_managers()
    #sm = network_management.socket_manager.SocketManager()
    #feeder_socket = network_management.socket_manager.SocketManager()
    
    #connect remote actuator
    while remote_actuator_offline:
        print("Connecting actuator")
        status = remote_hub_socket.connect(username_remote_hub)
        if status == online_status:
            remote_actuator_offline = False
        if status == offline_status:
            print("Registration attempt failed")
            time.sleep(1)

    #connect camera
    while camera_actuator_offline:
        print("Connecting camera")
        status = camera_socket.connect(username_camera)
        if status == online_status:
            camera_actuator_offline = False
        if status == offline_status:
            print("Registration attempt failed")
            time.sleep(1)

    while microphone_actuator_offline:
        print("Connecting microphone")
        status = microphone_socket.connect(username_microphone)
        if status == online_status:
            microphone_actuator_offline = False
        if status == offline_status:
            print("Registration attempt failed")
            time.sleep(1)

    # try and reveive all messages
    inner_while = True
    while inner_while:

        
            

        # receive and send camera actuator messages
        result = camera_socket.receive_message()
        if result:
            result_code = result[0]
            result_message = result[1]
            # result code 'OK' indicates a message was successfully received
            if result_code == 'OK':
                message = result[1]
                print(message)

                if result_message == "b'ON'":
                    GPIO.output(17, GPIO.HIGH)
                    result = camera_socket.send_message('OK ON')
                elif result_message == "b'OFF'":
                    GPIO.output(17, GPIO.LOW)
                    result = camera_socket.send_message('OK OFF')            
            elif result_code == 'SOCKET_EXCEPTION':
                print("Leaving inner while")
                inner_while = False
        else:
            print("Leaving inner while")
            inner_while = False
        result = camera_socket.send_message(reconnect_message)

        # receive and send microphone actuator messages
        result = microphone_socket.receive_message()
        if result:
            result_code = result[0]
            result_message = result[1]
            # result code 'OK' indicates a message was successfully received
            if result_code == 'OK':
                message = result[1]
                print(message)

                if result_message == "b'ON'":
                    GPIO.output(22, GPIO.HIGH)
                    result = microphone_socket.send_message('OK ON')
                elif result_message == "b'OFF'":
                    GPIO.output(22, GPIO.LOW)
                    result = microphone_socket.send_message('OK OFF')            
            elif result_code == 'SOCKET_EXEPTION':
                print("Leaving inner while")
                inner_while = False
        else:
            print("Leaving inner while")
            inner_while = False
        result = microphone_socket.send_message(reconnect_message)

        # receive and send remote actuator messages
        remote_result = remote_hub_socket.receive_message()
        if remote_result:
            remote_result_code = remote_result[0]
            if remote_result_code == 'OK':
                remote_message = remote_result[1]
                if remote_message == 'ON' and not remote_on:
                    try:
                        print("Going out of range of home hub...")
                        print("Turning on remote hub...")
                        remote_hub_process = subprocess.Popen(['python','remote_hub.py'])
                        remote_on = True
                        GPIO.output(11, GPIO.HIGH)
                        result = remote_hub_socket.send_message('OK ON')
                        remote_hub_socket.send_message('OK ON')
                    except Exception as e:
                        print("Exception when turning on remote hub: " + str(e))
                        inner_while = False
                elif remote_message == 'OFF':
                    try:
                        print("Pet has returned home")
                        print("Switching off remote hub...")
                        remote_on = False
                        inner_while = False
                        GPIO.output(11, GPIO.LOW)
                        #remote_hub_socket.send_message('OK OFF')
                        remote_hub_process.terminate()
                        #result = remote_hub_socket.send_message('OK OFF')
                    except Exception as e:
                        print("Exception when turning off remote hub: " + str(e))
                        inner_while = False
            if remote_result_code == 'SOCKET_EXCEPTION':
                print("Leaving inner while")
                inner_while = False
        else:
            print("Leaving inner while")
            inner_while = False
        result = remote_hub_socket.send_message(reconnect_message)
                
    #if remote_hub_socket.socket:
        #remote_hub_socket.socket.shutdown(socket.SHUT_RDWR)
        #remote_actuator_offline = True

