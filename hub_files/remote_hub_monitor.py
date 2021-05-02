import network_management.network_pickler as np
import json

class RemoteHubMonitor():

    on_message = 'ON'
    off_message = 'OFF'
    ok_state = 'OK'
    at_boundary = 'AT_BOUNDARY'
    pet_returned = 'PET_RETURNED'

    def __init__(self, clients, mqtt_manager):
        self.clients = clients
        self.mqtt_manager = mqtt_manager
        self.current_state = self.ok_state

    def message_remote_hub(self, actuator_message, mqtt_message):
        for client, name in self.clients.items():
            #print("Name: " + name)
            if name == 'remote_hub_actuator':
                #print("ATTEMPTING TO MESSAGE REMOTE HUB")
                pickled_message = np.pickle_message(actuator_message)
                client.send(pickled_message)
                self.mqtt_manager.publish_message(name, json.dumps(mqtt_message))

    def determine_network_health(self, message):
        if message == "OK":
            #print("Message == OK State")
            if self.current_state != self.ok_state:  #need to receive message to indicate hub is now off
                self.message_remote_hub(self.off_message, self.pet_returned)
            # Turn off remote hub
        if message == "AT BOUNDARY":
            #print("Message == at boundary")
            remote_hub_on = False
            for client, name in self.clients.items():
                if name == 'remote_hub':
                    remote_hub_on = True
            if not remote_hub_on:
                self.message_remote_hub(self.on_message, self.at_boundary)
