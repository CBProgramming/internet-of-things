import subprocess as sp
import datetime as dt

# amend the below boolean values to configure launch
launch_hub = True
launch_collar_controller = True
launch_feeder_actuator = True
launch_camera_outside1 = True
launch_camera_outside2 = True
launch_mock_publisher = False
launch_mock_subscriber = False
launch_mock_gps = False
# set run time (seconds )for automatic program termination
run_time = 120

# WARNING, stopping program manually may leave processes running in the backround
# which may affect the next run.  If you're experiencing bugs, check Task Manager
# and stop any Python background processes

# add additional python scripts below
SW_HIDE = 0
hide_info = sp.STARTUPINFO()
hide_info.dwFlags = sp.STARTF_USESHOWWINDOW
hide_info.wShowWindow = SW_HIDE
if launch_hub:
    hub_process = sp.Popen(['python','transport_hub.py'])
if launch_collar_controller:
    collar_controller_process = sp.Popen(['python','collar_controller.py'],
                              startupinfo=hide_info)
if launch_feeder_actuator:
    feeder_process = sp.Popen(['python','feeder_controller.py'])
                              #,startupinfo=hide_info)
if launch_camera_outside1:
    camera_outside1_process = sp.Popen(['python','actuator_camera_outside1.py']
                              ,startupinfo=hide_info
                                       )
if launch_camera_outside2:
    camera_outside2_process = sp.Popen(['python','actuator_camera_outside2.py']
                              ,startupinfo=hide_info
                              )    
if launch_mock_publisher:
    publish_process = sp.Popen(['python','mock_mqtt_publisher.py'],
                              startupinfo=hide_info)
if launch_mock_subscriber:
    subscriber_process = sp.Popen(['python','mock_mqtt_subscriber.py'],
                              startupinfo=hide_info)
if launch_mock_gps:
    mock_gps_process = sp.Popen(['python','mock_gps_sensor.py'],
                              startupinfo=hide_info
                                )
# terminate processes
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
                camera_outside1_process.terminate()
            except:
                None
            try:
                camera_outside2_process.terminate()
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
        
        
        
        
        
        
