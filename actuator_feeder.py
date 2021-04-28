import time
import network_management.socket_manager 
from EmulatorGUI_feeder import GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)



username_feeder = "feeder_actuator"
feeder_socket = network_management.socket_manager.SocketManager()

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

        #GPIO.cleanup()

           
         
       

    # Other result codes you might want to handle for:
    # 'INVALID_HEADER'  (This would indicate there is something wrong with the
    #                    network_config or socket_manager scripts)
    # 'NO_MESSAGES'  (This is an error you'll get whenever there's no messages
    #                 and it probably doesn't need handling as long as your
    #                 receive loop keeps running)
    # 'ERROR' (This is if something inexplicably goes wrong)
