import time
import network_management.socket_manager as sm
from EmulatorGUI import GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)

username = "speaker"
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
while True:
    # receive result, which is a list in the format [result_code, message]
    result = sm.receive_message(client_socket)
    
    result_code = result[0]
    result_message = result[1]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        print(message)

    if result_message == "b'ON'":
        GPIO.output(21, GPIO.HIGH)
    elif result_message == "b'OFF'":
        GPIO.output(21, GPIO.LOW)

        #GPIO.cleanup()

           
         
       

    # Other result codes you might want to handle for:
    # 'INVALID_HEADER'  (This would indicate there is something wrong with the
    #                    network_config or socket_manager scripts)
    # 'NO_MESSAGES'  (This is an error you'll get whenever there's no messages
    #                 and it probably doesn't need handling as long as your
    #                 receive loop keeps running)
    # 'ERROR' (This is if something inexplicably goes wrong)
