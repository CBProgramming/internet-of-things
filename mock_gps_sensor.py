import time, network_management.socket_manager
import mock_config.default_variables as dv

start_lat = dv.mock_latitude
start_long = dv.mock_longitude
one_foot = 0.018/5280
speed = 3

username = "gps_sensor"
sm = network_management.socket_manager.SocketManager()

# register socket with transport layer
status = 'OFFLINE'
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

#messaging loop
current_feet = 1
new_long = start_long
while True:
    time.sleep(1) # don't do this on real code (unless its relevant to simulating data)
    if current_feet > 50:
        print("Coming home")
        coming_home = True
    elif current_feet < 10:
        print("Leaving home")
        coming_home = False

    if coming_home:
        print("Reducing distance")
        print(current_feet)
        new_long = new_long - one_foot * speed
        current_feet = current_feet - speed
    else:
        print("Increasing distance")
        print(current_feet)
        new_long = new_long + one_foot * speed
        current_feet = current_feet + speed
    # attempt to send message, variable 'success' stores a boolean
    # value indicating if message sending was successful
    if sm:
        #print("attempting sending")
        message = [start_lat, new_long]
        success = sm.send_message(message)
        #print("success var = " + str(success))
