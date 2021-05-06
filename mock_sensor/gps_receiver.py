import math
import mock_config.default_variables as dv
import random as rng
from random import gauss as gauss

class GPSReceiver:
    def __init__(self):
        self.hub_latitude = dv.mock_latitude
        self.hub_longitude = dv.mock_longitude
        self.current_latitude = dv.mock_latitude
        self.current_longitude = dv.mock_longitude
        self.moving = False

    def get_position(self):
        self.update_position()
        return self.current_latitude, self.current_longitude

    def update_position(self):
        if rng.randint(1, 10) == 1:
            if self.moving:
                self.moving = False
            else:
                self.moving = True

        if self.moving:
            self.current_latitude = self.hub_latitude + (gauss(0, 5) / 6378000) * (180 / math.pi);
            self.current_longitude = self.hub_longitude + (gauss(0, 5) / 6378000) * (180 / math.pi) / math.cos(self.hub_latitude * math.pi / 180);


