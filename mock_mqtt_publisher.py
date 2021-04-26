import paho.mqtt.client as mqtt
import time
import random

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client_name_suffix = random.randint(0,999999999)

# set up client
broker = "broker.hivemq.com"
client = mqtt.Client("Mock_IoT_Phone_App_Publisher" + str(client_name_suffix))
client.connect(broker)

# define topics
camera_topic = "/petprotector/camera"
speaker_topic = "/petprotector/speaker"
gps_topic = "/petprotector/gps"
mock_actuator_1_topic = "/petprotector/Mock Actuator 1"
mock_actuator_2_topic = "/petprotector/Mock Actuator 2"

#subscribe to topics and start subscription loop
client.subscribe(gps_topic, 0)
client.on_message = on_message
client.loop_start() #handles reconnects automatically

#begin publishing loop
count = 1
message = ''
while True:
    if (count%2) == 0:
        message = 'ON'
    else:
        message = 'OFF'
    client.publish(mock_actuator_1_topic, message + ' ' + str(count + 100))
    client.publish(mock_actuator_2_topic, message + ' ' + str(count + 200))
    client.publish(speaker_topic, message)
    client.publish(camera_topic, message)
    print("count = " + str(count))
    count = count + 1
    time.sleep(1)

client.loop_stop()
