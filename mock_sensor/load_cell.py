import random as rng

class LoadCell:
    def __init__(self):
        self.current_weight = 0

    def get_weight(self):
        self.update_weight()
        return self.current_weight

    def update_weight(self):
        if self.current_weight > 0:
            amount_eaten = rng.randint(0, 12)
            if self.current_weight >= amount_eaten:
                self.current_weight = 0
            else:
                self.current_weight -= amount_eaten
        else:
            if rng.randint(0, 7) == 1:
                self.current_weight = 120


