import random as rng

class Thermistor:
    def __init__(self):
        self.current_temperature = 38.8

    def get_temperature(self):
        self.__update_temperature__()
        return self.current_temperature

    def __update_temperature__(self):
        if rng.randint(1, 2) == 1:
            if rng.randint(1, 2) % 2 == 0:
                self.current_temperature += 0.1
            else:
                self.current_temperature -= 0.1