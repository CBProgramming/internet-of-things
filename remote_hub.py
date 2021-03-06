import socket, select, queue
import paho.mqtt.client as mqtt
import network_management.network_config as nc
import hub_files.hub_read_socket_handler as hrsh
import hub_files.hub_exception_socket_handler as esh
import hub_files.hub_message_handler


s_timeout = nc.socket_timeout

print("Initialising remote hub...")

while True:
    
    try:
        port = nc.get_remote_port()
        ip_address = nc.get_ip()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip_address, port))
        server_socket.listen()
        rsh = hrsh.ReadSocketHandler(server_socket, 'remote')
        print("Listening for new devices...")
        while True:
            r_socks, w_socks, e_socks = select.select(rsh.sockets, [], rsh.sockets, s_timeout)
            rsh.handle_read_sockets(r_socks)
            if e_socks:
                esh.handle_exception_sockets(e_socks, rsh.sockets, rsh.clients, rsh.bsh)
            #print("Inner while complete!")
    except Exception as e:
        try:
            rsh.mqtt_manager.stop_client()
        except:
            None
        print("Remote hub exception: " + str(e))
        print("Rebooting...")
