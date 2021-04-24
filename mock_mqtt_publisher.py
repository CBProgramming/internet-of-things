import paho.mqtt.client as mqtt
import time

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# set up client
broker = "broker.hivemq.com"
client = mqtt.Client("IoT_Phone_App_Publisher")
client.connect(broker)

# define topics
camera_topic = "/petprotector/camera"
speaker_topic = "/petprotector/speaker"
gps_topic = "/petprotector/gps"

#subscribe to topics and start subscription loop
client.subscribe(gps_topic, 0)
client.on_message = on_message
client.loop_start() #handles reconnects automatically

#begin publishing loop
count = 1
while True:
    client.publish(camera_topic,'ON ' + str(count))
    client.publish(speaker_topic,'ON ' + str(count))
    print("count = " + str(count))
    count = count + 1
    time.sleep(1)

client.loop_stop()
