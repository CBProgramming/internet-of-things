import socket, select, queue
import paho.mqtt.client as mqtt
import network_config as nc
import hub_read_socket_handler as rsh
import hub_exception_socket_handler as esh
import hub_message_handler as hmh
import mqtt_manager as mm

socket_timeout = 1

while True:
    try:
        mqtt_manager = mm.MqttManager()
        port = nc.get_port()
        ip_address = nc.get_ip()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip_address, port))
        server_socket.listen()
        header_length = nc.get_header_length()
        sockets_list = [server_socket]
        clients = {}
        while True:
            read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list, socket_timeout)
            if read_sockets:
                sockets_list, clients = rsh.handle_read_sockets(read_sockets, server_socket, sockets_list, clients, mqtt_manager)
            if exception_sockets:
                sockets_list, clients = esh.handle_exception_sockets(exception_sockets, sockets_list, clients)
            clients = mqtt_manager.manage_queued_messages(clients)
    except Exception as e:
        mm.stop_client()
        print("Transport hub exception: " + str(e))
        print("Rebooting hub...")
