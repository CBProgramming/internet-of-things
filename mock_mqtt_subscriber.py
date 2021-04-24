import paho.mqtt.client as mqtt

# Change test_topic to test a specific topi
# "/petprotector/" is appended to front accordingly
test_topic = '#'
#test_topic = "Mock Sensor 1"

def on_message(client, obj, msg):
    print(str(msg.topic))
    print(str(msg.payload))
 
topic_head = "/petprotector/"
broker = "broker.hivemq.com"
client = mqtt.Client("Pet_Protector_Mock_Subscriber")
client.connect(broker)
client.subscribe(topic_head + test_topic, 0)
client.loop_start()
client.on_message = on_message
