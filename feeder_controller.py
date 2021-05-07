import time
import network_management.socket_manager
import mock_sensor.load_cell
from EmulatorGUI_feeder import GPIO

# import feeder_actuator_clock
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(9, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)

username_weight_sensor = "food_weight_sensor"
username_feeder = "feeder_actuator"

weight_sensor_socket = network_management.socket_manager.SocketManager()
feeder_socket = network_management.socket_manager.SocketManager()

weight_sensor = mock_sensor.load_cell.LoadCell()
GPIO.output(9, GPIO.HIGH)

feed_time = ""

# register socket with transport layer
status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = weight_sensor_socket.connect(username_weight_sensor)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = feeder_socket.connect(username_feeder)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

# messaging loop
while True:
    message = weight_sensor.get_weight()
    result = weight_sensor_socket.send_message(message)

    # receive result, which is a list in the format [result_code, message]
    result = feeder_socket.receive_message()
    # print(result)
    result_code = result[0]
    result_message = result[1]
    current_time = time.strftime("b'" + "%H:%M" + "'")

    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        print(message)

    if result_message == "b'ON'":
        GPIO.output(10, GPIO.HIGH)
        print("Dispensing food")
        result = feeder_socket.send_message('OK ON')
    elif result_message == "b'OFF'":
        print("Food dispensed")
        GPIO.output(10, GPIO.LOW)
        result = feeder_socket.send_message('OK OFF')
    else:
        if result_code == 'OK':
            message = result_message
            if ":" in message:
                feed_time = message
                result = feeder_socket.send_message('TIMER SET ' + feed_time)
                # print("the time is " + current_time)
                print("Feed time set " + feed_time)
            else:
                food_amount = message
                result = feeder_socket.send_message('WEIGHT SET ' + food_amount)
                print("Food weight set " + food_amount)

                if (current_time == feed_time):
                    GPIO.output(10, GPIO.HIGH)
                    print("Feeding time " + feed_time)
                    print("Dispensing food")
                    # feeding_now = "FEEDING"
                    result = feeder_socket.send_message('FEEDING ' + feed_time)
                    time.sleep(10)
                    print("Food dispensed")
                    GPIO.output(10, GPIO.LOW)

                else:
                    while True:
                        current_time != feed_time
                        # print(current_time)
                        # print(feed_time)
                        time.sleep(1)
                        current_time = time.strftime("b'" + "%H:%M" + "'")
                        if (current_time != feed_time):
                            None
                            # print(current_time)
                            # print(feed_time)
                            # print("not time yet")

                        else:
                            GPIO.output(10, GPIO.HIGH)
                            feeding_now = "FEEDING"
                            result = feeder_socket.send_message('FEEDING ' + feed_time)
                            print("Feeding time " + feed_time)
                            print("Dispensing food")
                            time.sleep(10)
                            print("Food dispensed")
                            GPIO.output(10, GPIO.LOW)

                            break

        # GPIO.cleanup()

# clock()


# Other result codes you might want to handle for:
# 'INVALID_HEADER'  (This would indicate there is something wrong with the
#                    network_config or socket_manager scripts)
# 'NO_MESSAGES'  (This is an error you'll get whenever there's no messages
#                 and it probably doesn't need handling as long as your
#                 receive loop keeps running)
# 'ERROR' (This is if something inexplicably goes wrong)
