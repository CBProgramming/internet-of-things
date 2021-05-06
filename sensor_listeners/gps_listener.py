import time
import network_management.socket_manager
import mock_sensor.gps_receiver

username = "Mock Sensor 1"
sm = network_management.socket_manager.SocketManager()
gpsr = mock_sensor.gps_receiver.GPSReceiver()

# register socket with transport layer
status = 'OFFLINE'
while True:
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

    while True:
        latitude, longitude = gpsr.get_position()
        message = [latitude, longitude]

        time.sleep(1)

        # attempt to send message, variable 'result' stores a boolean
        # value indicating if message sending was successful
        result = sm.send_message(message)

        # POSSIBLE RESULTS
        # 'OK'
        # 'INVALID MESSAGE FORMAT'
        # 'OFFLINE'    This one means 5 recconect attempts were tried on both hubs

        status = 'OFFLINE' if result == 'OFFLINE' else 'ONLINE'