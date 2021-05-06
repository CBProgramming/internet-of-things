import random as rng

class LoadCell:
    def __init__(self):
        self.current_battery_level = 100
        self.charging = False

    def get_battery_level(self):
        self.update_battery_level()
        return self.current_battery_level

    def update_battery_level(self):
        if (rng.randint(0, self.current_battery_level)) / 10 == 0:
            if not self.charging:
                self.charging = True

        if (rng.randint(0, 100 - self.current_battery_level)) / 10 == 0:
            if self.charging:
                self.charging = False

        if self.charging:
            if self.current_battery_level < 100:
                self.current_battery_level += 1
        else:
            if self.current_battery_level > 0:
                self.current_battery_level -= 1