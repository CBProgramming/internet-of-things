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

#speaker_topic = "/petprotector/speaker_actuator"
#microphone_topic = "/petprotector/microphone_actuator"
#feeder_topic = "/petprotector/feeder_actuator"
#remote_hub_topic = "/petprotector/remote_hub_actuator"
#camera_outside1_topic = "/petprotector/camera_outside1_actuator"
#camera_outside2_topic = "/petprotector/camera_outside2_actuator"
gps_topic = "/petprotector/gps"
#mock_actuator_1_topic = "/petprotector/Mock Actuator 1"
#mock_actuator_2_topic = "/petprotector/Mock Actuator 2"
#dispencing_food_topic = "/petprotector/feeder_actuator/dispencing_food"
#food_dispenced_topic = "/petprotector/feeder_actuator/food_dispenced"
camera_data_topic = "/petprotector/camera_actuator/data"
feeding_time_topic = "/petprotector/feeder_actuator/feeding_times"
meal_size_topic = "/petprotector/feeder_actuator/meal_size"
feeder_actuator_data = "/petprotector/feeder_actuator/data"
collar_battery_sensor = "/petprotector/collar_battery_sensor"
gps_sensor = "/petprotector/gps_sensor"
motion_sensor = "/petprotector/motion_sensor"
temperature_sensor = "/petprotector/temperature_sensor"
food_weight_topic = "/petprotector/food_weight_sensor"
microphone_data = "/petprotector/microphone_actuator/data"
speaker_data = "/petprotector/speaker_actuator/data"
user_notif = "/petprotector/user_notification"


#subscribe to topics and start subscription loop
client.subscribe(gps_topic, 0)
client.on_message = on_message
client.loop_start() #handles reconnects automatically

#begin publishing loop
count = 1
message = ''
messageT = ''
messageM = ''
messageD = ''
messageD2 = ''
messageC = ''
messageG = ''
messageMO = ''
messageTE = ''
messageFWS = ''
messageSPE = ''
messageMIC = ''
messageNOT = ''
while True:
    if (count%2) == 0:
        message = 'ON'
        messageT = "13:00"
        messageM = "200"
        messageD = "TIMER SET " + "19:20"
        messageD2 = "WEIGHT SET " + "200"
        messageC = "20"
        messageG = "OUT OF BOUNDS"
        messageMO = "TOO FAST"
        messageTE = "TOO HOT"
        messageFWS = "500"
        messageSPE = "ON"
        messageMIC = "OFF"
        messageNOT = "NOT1"
    else:
        message = 'OFF'
        messageT = "14:00"
        messageM = "500"
        messageD = "TIMER SET " + "19:25"
        messageD2 = "WEIGHT SET " + "250"
        messageC = "25"
        messageG = "In Bounds"
        messageMO = "Nice steady"
        messageTE = "TOO COLD"
        messageFWS = "499"
        messageSPE = "OFF"
        messageMIC = "ON"
        messageNOT = "NOT2"
    #client.publish(mock_actuator_1_topic, message + ' ' + str(count + 100))
    #client.publish(mock_actuator_2_topic, message + ' ' + str(count + 200))
    client.publish(camera_data_topic, message)
    client.publish(feeding_time_topic, messageT)
    client.publish(meal_size_topic, messageM)
    client.publish(feeder_actuator_data, messageD)
    client.publish(feeder_actuator_data, messageD2)
    client.publish(collar_battery_sensor, messageC)
    client.publish(gps_sensor, messageG)
    client.publish(motion_sensor, messageMO)
    client.publish(temperature_sensor, messageTE)
    client.publish(food_weight_topic, messageFWS)
    client.publish(microphone_data, messageMIC)
    client.publish(speaker_data, messageSPE)
    client.publish(user_notif, messageNOT)
    #client.publish(speaker_topic, message)
    #client.publish(microphone_topic, message)

    #client.publish(feeder_topic, message)
    #client.publish(feeding_time_topic,message)
    #client.publish(meal_size_topic,message)
    #client.publish(dispencing_food_topic,message)
    #client.publish(food_dispenced_topic,feed_time)
    #client.publish(remote_hub_topic, message)
    #client.publish(camera_outside1_topic, message)
    #client.publish(camera_outside2_topic, message)
    if count == 15:
         #automatically calculate time one minute from now
        feed_time = str((dt.datetime.now() + dt.timedelta(0,60)).strftime("%H:%M"))
        client.publish(feeding_time_topic, feed_time)
        client.publish(meal_size_topic, "300")
    print("count = " + str(count))
    count = count + 1
    time.sleep(1)

client.loop_stop()
