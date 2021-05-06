import random as rng
from random import gauss as gauss

class Accelerometer:
    def __init__(self):
        self.current_acceleration = [0, 0, 0]
        self.moving = False

    def get_acceleration(self):
        self.update_acceleration()
        return self.current_acceleration

    def update_acceleration(self):
        if rng.randint(1, 10) == 1:
            if self.moving:
                self.moving = False
            else:
                self.moving = True

        if self.moving:
            self.current_acceleration = [gauss(0, 10), gauss(0, 10), gauss(0, 10) + 9.8]
        else:
            self.current_acceleration = [0, 0, 9.8]



