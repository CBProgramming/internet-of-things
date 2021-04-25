import socket, select, queue
import paho.mqtt.client as mqtt
import network_config as nc
import hub_read_socket_handler as hrsh
import hub_exception_socket_handler as esh
import hub_message_handler


socket_timeout = 1

while True:
    try:
        port = nc.get_port()
        ip_address = nc.get_ip()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip_address, port))
        server_socket.listen()
        header_length = nc.get_header_length()
        rsh = hrsh.ReadSocketHandler(server_socket)
        while True:
            r_socks, w_socks, e_socks = select.select(rsh.sockets, [], rsh.sockets, socket_timeout)
            if r_socks:
                rsh.handle_read_sockets(r_socks)
            if e_socks:
                esh.handle_exception_sockets(e_socks, rsh.sockets, rsh.clients)  
    except Exception as e:
        rsh.mqtt_manager.stop_client()
        print("Transport hub exception: " + str(e))
        print("Rebooting hub...")
