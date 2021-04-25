import queue
import paho.mqtt.client as mqtt

class MqttManager:
    def __init__(self):

        def get_device(topic):
            head = topic[:len(self.topic_head)]
            if head == self.topic_head:
                device = topic[len(self.topic_head):]
                return device
            return None

        def on_message(client, obj, msg):
            topic_payload = msg.topic
            device = get_device(topic_payload)
            if device:
                self.mqtt_queue.put([str(device),str(msg.payload)])
        
        self.mqtt_queue = queue.Queue()
        self.topic_head = "/petprotector/"
        broker = "broker.hivemq.com"
        self.client = mqtt.Client("Pet_Protector_Home_Hub")
        self.client.connect(broker)
        all_topics = self.topic_head + '#'
        self.client.subscribe(all_topics, 0)
        self.client.loop_start()
        self.client.on_message = on_message

    def handle_messages(self, mqtt_messages):
        for message in mqtt_messages:
            self.hmh.handle_mqtt_message(message)

    def manage_queued_messages(self):
        i = 0
        mqtt_messages = []
        while i < self.mqtt_queue.qsize():
            mqtt_messages.append(self.mqtt_queue.get())
            i = i + 1
        self.handle_messages(mqtt_messages)

    def stop_client(self):
        print("Stopping mqtt loop")
        self.client.loop_stop()

    def publish_message(self, topic_key, message):
        topic = self.topic_head + topic_key
        self.client.publish(topic,message)
