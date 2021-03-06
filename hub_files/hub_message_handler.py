import socket, json
import network_management.network_pickler as np
import hub_files.remote_hub_monitor
import hub_files.gps_range_calculator as grc

class HubMessageHandler():

    def __init__(self, clients, mqtt_manager, rsh):
        self.data_string = '/data'
        self.clients = clients
        self.mqtt_manager = mqtt_manager
        self.mqtt_manager.hmh = self
        self.rhm = hub_files.remote_hub_monitor.RemoteHubMonitor(self.clients, self.mqtt_manager)
        self.rsh = rsh
        self.gps_count = 0
        self.gps_trigger = 5

    def handle_network_message(self, notified_socket, message):
        try:
            #print("Handling network message")
            sensor = self.clients[notified_socket]
            #print("Sensor: " + str(sensor))
            #if sensor == 'gps_sensor':
                #print("GPS received as: " + str(message))
                #print(type(message))
            if sensor == 'camera_actuator' or sensor == 'microphone_actuator' or sensor == 'speaker_actuator' or sensor == 'feeder_actuator':
                self.mqtt_manager.publish_message(sensor + self.data_string, json.dumps(message))
            elif sensor == 'gps_sensor':
                if self.gps_count == 0:
                    try:
                        gps_lat = message[0]
                        gps_lon = message[1]
                        self.mqtt_manager.publish_message('gps/lat', json.dumps(gps_lat))
                        self.mqtt_manager.publish_message('gps/lng', json.dumps(gps_lon))
                        
                    except:
                        None
                self.mqtt_manager.publish_message(sensor, json.dumps(message))
                self.gps_count = self.gps_count + 1
                if self.gps_count >= self.gps_trigger:
                    self.gps_count = 0
            else:    
                self.mqtt_manager.publish_message(sensor, json.dumps(message))
        except Exception as e:
            print("Hub message publish error: " + str(e))
        device = self.clients[notified_socket]
        if device == 'range_sensor':
            self.rhm.determine_network_health(message)
            

    def handle_mqtt_message(self, message):
        #print("HUB_MESSAGE_HANDLER - MQTT message received: " + str(message[1]))
        message_key = message[0]
        #print("Message key is: " + message_key)
        data = message[1]
        if message_key == 'gps_sensor':
            string_data = str(data)
            string_data = string_data[3:-2]
            #print("String Data: " + string_data)
            result = grc.translate_gps(string_data)
            #print("Result: " + str(result))
            if result == 'OK':
                if self.rsh.in_range == False:
                    print("Pet within acceptable range of home hub")
                    self.rsh.in_range = True
            if result == 'AT BOUNDARY':
                for key, value in self.clients.items():
                    if value == "camera_outside1_actuator" or value == "camera_outside2_actuator":
                        pickled_message = np.pickle_message("b'ON'")
                        key.send(pickled_message)
            else:
                for key, value in self.clients.items():
                    if value == "camera_outside1_actuator" or value == "camera_outside2_actuator":
                        pickled_message = np.pickle_message("b'OFF'")
                        key.send(pickled_message)
        #print("Handling MQTT message: " + str(data))
        for key, value in self.clients.items():
            if message_key == value or self.is_message_for_feeder(message_key, value):
                #print("Sending on key: " + str(message_key))
                pickled_message = np.pickle_message(data)
                #print(key)
                try:
                    key.send(pickled_message)
                except:
                    print("HMH: Error when sending message on key: " + str(value))
                #print("Sent on key: " + str(message_key))
                
            
    def is_message_for_feeder(self, message_key, value):
        if value == 'feeder_actuator':
            if (message_key == 'feeder_actuator/feeding_times' or
                message_key == 'feeder_actuator/meal_size' or
                message_key == 'feeder_actuator'):
                return True
        return False
        
                
        #print("Finished handling MQTT messages")

    def send_to_all(self, notified_socket, message):
        for client_socket in self.clients:
            if client_socket != notified_socket:
                pickled_message = np.pickle_message(message)
                print(pickled_message)
                client_socket.send(pickled_message)
                
    
