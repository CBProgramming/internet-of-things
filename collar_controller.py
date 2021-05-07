import subprocess
import time
import network_management.socket_manager
import mock_sensor.accelerometer
import mock_sensor.battery_level_indicator
import mock_sensor.gps_receiver
import mock_sensor.microphone
import mock_sensor.thermistor
from EmulatorGUI_controller import GPIO
import mock_config.default_variables as dv

start_lat = dv.mock_latitude
start_long = dv.mock_longitude
one_foot = 0.018/5280
speed = 3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

# GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)

username_battery_sensor = "collar_battery_sensor"
username_gps_sensor = "gps_sensor"
username_motion_sensor = "motion_sensor"
username_sound_sensor = "sound_sensor"
username_temperature_sensor = "temperature_sensor"

# username_feeder = "feeder_actuator"
username_remote_hub = "remote_hub_actuator"
username_camera = "camera_actuator"
username_microphone = "microphone_actuator"
username_speaker = "speaker_actuator"

battery_sensor_socket = network_management.socket_manager.SocketManager()
gps_sensor_socket = network_management.socket_manager.SocketManager()
motion_sensor_socket = network_management.socket_manager.SocketManager()
sound_sensor_socket = network_management.socket_manager.SocketManager()
temperature_sensor_socket = network_management.socket_manager.SocketManager()

# sm = network_management.socket_manager.SocketManager()
# feeder_socket = network_management.socket_manager.SocketManager()
remote_hub_socket = network_management.socket_manager.SocketManager()
camera_socket = network_management.socket_manager.SocketManager()
microphone_socket = network_management.socket_manager.SocketManager()
speaker_socket = network_management.socket_manager.SocketManager()

battery_sensor = mock_sensor.battery_level_indicator.BatteryIndicator()
GPIO.output(18, GPIO.HIGH)
gps_sensor = mock_sensor.gps_receiver.GPSReceiver()
GPIO.output(23, GPIO.HIGH)
motion_sensor = mock_sensor.accelerometer.Accelerometer()
GPIO.output(24, GPIO.HIGH)
sound_sensor = mock_sensor.microphone.Microphone()
GPIO.output(25, GPIO.HIGH)
temperature_sensor = mock_sensor.thermistor.Thermistor()
GPIO.output(8, GPIO.HIGH)


remote_on = False
remote_hub_script = 'remote_hub.py'
reconnect_message = 'let me in'

# register socket with transport layer
status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register battery level sensor")
    status = battery_sensor_socket.connect(username_battery_sensor)
    # print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register gps sensor")
    status = gps_sensor_socket.connect(username_gps_sensor)
    # print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register motion sensor")
    status = motion_sensor_socket.connect(username_motion_sensor)
    # print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register sound sensor")
    status = sound_sensor_socket.connect(username_sound_sensor)
    # print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register temperature sensor")
    status = temperature_sensor_socket.connect(username_temperature_sensor)
    # print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

"""status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register")
    status = feeder_socket.connect(username_feeder)
    print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
                             ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)"""

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register remote hub actuator")
    status = remote_hub_socket.connect(username_remote_hub)
    # print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register camera")
    status = camera_socket.connect(username_camera)
    # print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register microphone")
    status = microphone_socket.connect(username_microphone)
    # print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

status = 'OFFLINE'
while status == 'OFFLINE':
    print("Attempting to register speaker")
    status = speaker_socket.connect(username_speaker)
    # print(status)
    if status == 'OFFLINE':  ## sm tries five times on both hubs
        ## before returning an 'OFFLINE' result
        print("Registration attempt failed")
        time.sleep(1)

    # registered = False
# while not registered:
# registered = sm.register(username, feeder_socket)
# registered = sm.register(username, remote_hub_socket)
# registered = sm.register(username, camera_socket)
# registered = sm.register(username, microphone_socket)
# registered = sm.register(username, speaker_socket)
# if not registered:
# print("Registration attempt failed")
# time.sleep(1) # this might need better handling as currently it just
# spams the network every second

current_feet = 1
new_long = start_long

# messaging loop
while True:
    time.sleep(1)

    message = battery_sensor .get_battery_level()
    result = battery_sensor_socket.send_message(message)

    #latitude, longitude = gps_sensor.get_position()
    #message = [latitude, longitude]
    #result = gps_sensor_socket.send_message(message)

    if current_feet > 50:
        #print("Coming home")
        coming_home = True
    elif current_feet < 10:
        #print("Leaving home")
        coming_home = False

    if coming_home:
        #print("Reducing distance")
        #print(current_feet)
        new_long = new_long - one_foot * speed
        current_feet = current_feet - speed
    else:
        #print("Increasing distance")
        #print(current_feet)
        new_long = new_long + one_foot * speed
        current_feet = current_feet + speed
    # attempt to send message, variable 'success' stores a boolean
    # value indicating if message sending was successful
    if gps_sensor_socket:
        #print("attempting sending")
        message = [start_lat, new_long]
        success = gps_sensor_socket.send_message(message)
        

    message = motion_sensor.get_acceleration()
    result = motion_sensor_socket.send_message(message)

    message = sound_sensor.get_sound()
    result = sound_sensor_socket.send_message(message)

    message = temperature_sensor.get_temperature()
    result = temperature_sensor_socket.send_message(message)

    

    # receive result, which is a list in the format [result_code, message]
    """result = feeder_socket.receive_message()

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
        None"""

    # receive result, which is a list in the format [result_code, message]
    result = remote_hub_socket.receive_message()

    result_code = result[0]
    result_message = result[1]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        # print(message)

        if message == 'ON' and not remote_on:
            try:
                print("Going out of range of home hub...")
                print("Turning on remote hub...")
                SW_HIDE = 5
                show_info = subprocess.STARTUPINFO()
                show_info.dwFlags = subprocess.STARTF_USESHOWWINDOW
                show_info.wShowWindow = SW_HIDE
                remote_hub_process = subprocess.Popen(['python', 'remote_hub.py'],
                                                      creationflags=subprocess.CREATE_NEW_CONSOLE)
                remote_on = True
                GPIO.output(11, GPIO.HIGH)
                result = remote_hub_socket.send_message('OK ON')
                remote_hub_socket.send_message('OK ON')
            except Exception as e:
                print("Exception when turning on remote hub: " + str(e))
                inner_while = False
        elif message == 'OFF':
            try:
                print("Pet has returned home")
                print("Switching off remote hub...")
                remote_on = False
                inner_while = False
                GPIO.output(11, GPIO.LOW)
                # remote_hub_socket.send_message('OK OFF')
                remote_hub_process.terminate()
                result = remote_hub_socket.send_message('OK OFF')
            except Exception as e:
                print("Exception when turning off remote hub: " + str(e))
                inner_while = False
    elif result_code == 'SOCKET_EXEPTION':
        None
    result = remote_hub_socket.send_message(reconnect_message)

    # receive result, which is a list in the format [result_code, message]
    result = camera_socket.receive_message()
    result_code = result[0]
    result_message = result[1]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        # print(message)

        if result_message == "b'ON'":
            GPIO.output(17, GPIO.HIGH)
            result = camera_socket.send_message('OK ON')
        elif result_message == "b'OFF'":
            GPIO.output(17, GPIO.LOW)
            result = camera_socket.send_message('OK OFF')
    elif result_code == 'SOCKET_EXEPTION':
        None
    result = camera_socket.send_message(reconnect_message)

    # receive result, which is a list in the format [result_code, message]
    result = microphone_socket.receive_message()

    result_code = result[0]
    result_message = result[1]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        # print(message)

        if result_message == "b'ON'":
            GPIO.output(22, GPIO.HIGH)
            result = microphone_socket.send_message('OK ON')
        elif result_message == "b'OFF'":
            GPIO.output(22, GPIO.LOW)
            result = microphone_socket.send_message('OK OFF')
    elif result_code == 'SOCKET_EXEPTION':
        None
    result = microphone_socket.send_message(reconnect_message)

    # receive result, which is a list in the format [result_code, message]
    result = speaker_socket.receive_message()

    result_code = result[0]
    result_message = result[1]
    # result code 'OK' indicates a message was successfully received
    if result_code == 'OK':
        message = result[1]
        # print(message)

        if result_message == "b'ON'":
            GPIO.output(27, GPIO.HIGH)
            result = speaker_socket.send_message('OK ON')
        elif result_message == "b'OFF'":
            GPIO.output(27, GPIO.LOW)
            result = speaker_socket.send_message('OK OFF')
    elif result_code == 'SOCKET_EXEPTION':
        None
    result = speaker_socket.send_message(reconnect_message)

    # GPIO.cleanup()

    # Other result codes you might want to handle for:
    # 'INVALID_HEADER'  (This would indicate there is something wrong with the
    #                    network_config or socket_manager scripts)
    # 'NO_MESSAGES'  (This is an error you'll get whenever there's no messages
    #                 and it probably doesn't need handling as long as your
    #                 receive loop keeps running)
    # 'ERROR' (This is if something inexplicably goes wrong)
