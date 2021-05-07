import paho.mqtt.client as mqtt
import time
import random
import datetime as dt

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client_name_suffix = random.randint(0,999999999)

# set up client
broker = "broker.hivemq.com"
client = mqtt.Client("Mock_IoT_Phone_App_Publisher" + str(client_name_suffix))
client.connect(broker)

# define topics
camera_topic = "/petprotector/camera_actuator"
speaker_topic = "/petprotector/speaker_actuator"
microphone_topic = "/petprotector/microphone_actuator"
feeder_topic = "/petprotector/feeder_actuator"
remote_hub_topic = "/petprotector/remote_hub_actuator"
camera_outside1_topic = "/petprotector/camera_outside1_actuator"
camera_outside2_topic = "/petprotector/camera_outside2_actuator"
gps_topic = "/petprotector/gps"
mock_actuator_1_topic = "/petprotector/Mock Actuator 1"
mock_actuator_2_topic = "/petprotector/Mock Actuator 2"
feeding_time_topic = "/petprotector/feeder_actuator/feeding_times"
meal_size_topic = "/petprotector/feeder_actuator/meal_size"
dispencing_food_topic = "/petprotector/feeder_actuator/dispencing_food"
#food_dispenced_topic = "/petprotector/feeder_actuator/food_dispenced"
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
    #client.publish(mock_actuator_1_topic, message + ' ' + str(count + 100))
    #client.publish(mock_actuator_2_topic, message + ' ' + str(count + 200))
    client.publish(camera_topic, message)
    client.publish(speaker_topic, message)
    client.publish(microphone_topic, message)
    client.publish(feeder_topic, message)
    client.publish(feeding_time_topic,message)
    client.publish(meal_size_topic,message)
    client.publish(dispencing_food_topic,message)
    #client.publish(food_dispenced_topic,feed_time)
    #client.publish(remote_hub_topic, message)
    #client.publish(camera_outside1_topic, message)
    #client.publish(camera_outside2_topic, message)
   # if count == 15:
         #automatically calculate time one minute from now
       # feed_time = str((dt.datetime.now() + dt.timedelta(0,60)).strftime("%H:%M"))
       # client.publish(feeding_time_topic, feed_time)
       # client.publish(meal_size_topic, "300")
    print("count = " + str(count))
    count = count + 1
    time.sleep(1)

client.loop_stop()
