import time
import network_management.socket_manager 
from EmulatorGUI import GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)

username_feeder = "feeder_actuator"
username_remote_hub = "remote_hub_actuator"
username_camera = "camera_actuator"
username_microphone = "microphone_actuator"
username_speaker = "speaker_actuator"
#sm = network_management.socket_manager.SocketManager()
feeder_socket = network_management.socket_manager.SocketManager()
remote_hub_socket = network_management.socket_manager.SocketManager()
camera_socket = network_management.socket_manager.SocketManager()
microphone_socket = network_management.socket_manager.SocketManager()
speaker_socket = network_management.socket_manager.SocketManager()

# register socket with transport layer
status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = feeder_socket.connect(username_feeder)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
                             ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = remote_hub_socket.connect(username_remote_hub)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
                             ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)
        
status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = camera_socket.connect(username_camera)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
                             ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = microphone_socket.connect(username_microphone)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
                             ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = speaker_socket.connect(username_speaker)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
                             ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)        

#registered = False
#while not registered:
    #registered = sm.register(username, feeder_socket)
    #registered = sm.register(username, remote_hub_socket)
    #registered = sm.register(username, camera_socket)
    #registered = sm.register(username, microphone_socket)
    #registered = sm.register(username, speaker_socket)
    #if not registered:
        #print("Registration attempt failed")
        #time.sleep(1) # this might need better handling as currently it just
                      # spams the network every second

#messaging loop
while True:

    # receive result, which is a list in the format [result_code, message]
    result = feeder_socket.receive_message()
    
    result_code = result[0]
    result_message = result[1]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        print(message)

        if result_message == "b'ON'":
            GPIO.output(10, GPIO.HIGH)
            result = feeder_socket.send_message('OK ON')
        elif result_message == "b'OFF'":
            GPIO.output(10, GPIO.LOW)
            result = feeder_socket.send_message('OK OFF')            
    elif result_code == 'SOCKET_EXEPTION':
        None
    
    # receive result, which is a list in the format [result_code, message]
    result = remote_hub_socket.receive_message()
    
    result_code = result[0]
    result_message = result[1]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        print(message)

        if result_message == "b'ON'":
            GPIO.output(11, GPIO.HIGH)
            result = remote_hub_socket.send_message('OK ON')
        elif result_message == "b'OFF'":
            GPIO.output(11, GPIO.LOW)
            result = remote_hub_socket.send_message('OK OFF')            
    elif result_code == 'SOCKET_EXEPTION':
        None

        
    # receive result, which is a list in the format [result_code, message]
    result = camera_socket.receive_message()
    
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
    elif result_code == 'SOCKET_EXEPTION':
        None
        
        
    # receive result, which is a list in the format [result_code, message]
    result = microphone_socket.receive_message()
    
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
        None
        

    # receive result, which is a list in the format [result_code, message]
    result = speaker_socket.receive_message()
    
    result_code = result[0]
    result_message = result[1]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        print(message)

        if result_message == "b'ON'":
            GPIO.output(27, GPIO.HIGH)
            result = speaker_socket.send_message('OK ON')
        elif result_message == "b'OFF'":
            GPIO.output(27, GPIO.LOW)
            result = speaker_socket.send_message('OK OFF')        
    elif result_code == 'SOCKET_EXEPTION':
        None
        
        
        #GPIO.cleanup()

           
         
       

    # Other result codes you might want to handle for:
    # 'INVALID_HEADER'  (This would indicate there is something wrong with the
    #                    network_config or socket_manager scripts)
    # 'NO_MESSAGES'  (This is an error you'll get whenever there's no messages
    #                 and it probably doesn't need handling as long as your
    #                 receive loop keeps running)
    # 'ERROR' (This is if something inexplicably goes wrong)
