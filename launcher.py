import subprocess as sp
import datetime as dt

# amend the below boolean values to configure launch
launch_hub = True
launch_collar_controller = True
launch_feeder_actuator = True
launch_mock_publisher = True
launch_mock_subscriber = False
launch_mock_gps = True

run_time = 120

# do not edit
SW_HIDE = 0
hide_info = sp.STARTUPINFO()
hide_info.dwFlags = sp.STARTF_USESHOWWINDOW
hide_info.wShowWindow = SW_HIDE
if launch_hub:
    hub_process = sp.Popen(['python','transport_hub.py'])
if launch_collar_controller:
    collar_controller_process = sp.Popen(['python','actuator_controller.py'])
if launch_feeder_actuator:
    feeder_process = sp.Popen(['python','actuator_feeder.py'],
                              startupinfo=hide_info)
if launch_mock_publisher:
    publish_process = sp.Popen(['python','mock_mqtt_publisher.py'],
                              startupinfo=hide_info)
if launch_mock_subscriber:
    subscriber_process = sp.Popen(['python','mock_mqtt_subscriber.py'],
                              startupinfo=hide_info)
if launch_mock_gps:
    mock_gps_process = sp.Popen(['python','mock_gps_sensor.py'],
                              startupinfo=hide_info)

running = True
finish_time = (dt.datetime.now() + dt.timedelta(0,run_time)).strftime("%H:%M:%S")
print("Finish time: " + str(finish_time))
while running:
    now = dt.datetime.now().strftime("%H:%M:%S")
    if finish_time == now:
        while True:
            try:
                hub_process.terminate()
            except:
                None
            try:
                collar_controller_process.terminate()
            except:
                None
            try:
                feeder_process.terminate()
            except:
                None
            try:
                publish_process.terminate()
            except:
                None
            try:
                subscriber_process.terminate()
            except:
                None
            try:
                mock_gps_process.terminate()
            except:
                None
        
        
        
        
        
        
