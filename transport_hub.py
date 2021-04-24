import socket, select, queue
import paho.mqtt.client as mqtt
import network_config as nc
import hub_read_socket_handler as rsh
import hub_exception_socket_handler as esh

socket_timeout = 1

topic_head = "/petprotector/"
mqtt_queue = queue.Queue()
mqtt_messages = []

def get_device(topic):
    head = topic[:len(topic_head)]
    if head == topic_head:
        device = topic[len(topic_head):]
        return device
    return None

def on_message(client, obj, msg):
    topic_payload = msg.topic
    device = get_device(topic_payload)
    if device:
        mqtt_queue.put([str(device),str(msg.payload)])
        

def get_mqtt_messages_in_queue():
    i = 0
    while i < mqtt_queue.qsize():
        mqtt_messages.append(mqtt_queue.get())
        i = i + 1
    
def setup_mqtt_client():
    broker = "broker.hivemq.com"
    client = mqtt.Client("Pet_Protector_Home_Hub")
    client.connect(broker)
    all_topics = topic_head + '#'
    client.subscribe(all_topics, 0)
    client.loop_start()
    client.on_message = on_message
    return client

def cleanup_handled_mqtt_messages(handled_messages, lock):
    None
    # need to add lock, remove handled_messages from mqtt_messages and unlock
    #might actually need to do a queue

while True:
    try:
        mqtt_client = setup_mqtt_client()
        port = nc.get_port()
        ip_address = nc.get_ip()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate socket
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # setup reusable address
        server_socket.bind((ip_address, port))
        server_socket.listen()
        header_length = nc.get_header_length()
        sockets_list = [server_socket]
        clients = {}
        while True:
            read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list, socket_timeout)
            get_mqtt_messages_in_queue()
            print(mqtt_messages)
            if read_sockets:
                sockets_list, clients = rsh.handle_read_sockets(read_sockets, server_socket, sockets_list, clients)
            if exception_sockets:
                sockets_list, clients = esh.handle_exception_sockets(exception_sockets, sockets_list, clients)
            #need to process mqtt messages before clearing
            mqtt_messages = []
            
    except Exception as e:
        client.loop_stop()
        print("Transport hub exception: " + str(e))
        print("Rebooting hub...")
