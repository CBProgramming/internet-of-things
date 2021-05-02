import time
import network_management.socket_manager 
from EmulatorGUI_camera_outside2 import GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)



username_camera_outside2 = "camera_outside1_actuator"
camera_outside2_socket = network_management.socket_manager.SocketManager()

# register socket with transport layer
status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = camera_outside2_socket.connect(username_camera_outside2)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
                             ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

#messaging loop
while True:
    # receive result, which is a list in the format [result_code, message]
    result = camera_outside2_socket.receive_message()
    
    result_code = result[0]
    result_message = result[1]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        print(message)

    if result_message == "b'ON'":
        GPIO.output(23, GPIO.HIGH)
        result = camera_outside2_socket.send_message('OK ON')
    elif result_message == "b'OFF'":
        GPIO.output(23, GPIO.LOW)
        result = camera_outside2_socket.send_message('OK OFF')

        #GPIO.cleanup()

           
         
       

    # Other result codes you might want to handle for:
    # 'INVALID_HEADER'  (This would indicate there is something wrong with the
    #                    network_config or socket_manager scripts)
    # 'NO_MESSAGES'  (This is an error you'll get whenever there's no messages
    #                 and it probably doesn't need handling as long as your
    #                 receive loop keeps running)
    # 'ERROR' (This is if something inexplicably goes wrong)
