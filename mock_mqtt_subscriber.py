import paho.mqtt.client as mqtt
import random

# Change test_topic to test a specific topi
# "/petprotector/" is appended to front accordingly
#test_topic = 'feeder_actuator'
#test_topic = "Mock Sensor 1"
test_topic = '#'  # subscribe to all

def on_message(client, obj, msg):
    print(str(msg.topic))
    print(str(msg.payload))

client_name_suffix = random.randint(0,999999999)
topic_head = "/petprotector/"
broker = "broker.hivemq.com"
client = mqtt.Client("Pet_Protector_Mock_Subscriber" + str(client_name_suffix))
client.connect(broker)
client.subscribe(topic_head + test_topic, 0)
client.loop_start()
client.on_message = on_message
