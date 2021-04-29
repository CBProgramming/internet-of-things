import socket, select, queue
import paho.mqtt.client as mqtt
import network_management.network_config as nc
import hub_files.hub_read_socket_handler as hrsh
import hub_files.hub_exception_socket_handler as esh
import hub_files.hub_message_handler


socket_timeout = 0.25

print("Initialising home hub...")

while True:
    try:
        port = nc.get_port()
        ip_address = nc.get_ip()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip_address, port))
        server_socket.listen()
        rsh = hrsh.ReadSocketHandler(server_socket, 'home')
        while True:
            r_socks, w_socks, e_socks = select.select(rsh.sockets, [], rsh.sockets, socket_timeout)
            rsh.handle_read_sockets(r_socks)
            if e_socks:
                esh.handle_exception_sockets(e_socks, rsh.sockets, rsh.clients, rsh.bsh)
            #print("Inner while complete!")
    except Exception as e:
        try:
            rsh.mqtt_manager.stop_client()
        except:
            None
        print("Transport hub exception: " + str(e))
        print("Rebooting hub...")
