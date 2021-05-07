import random as rng

class LoadCell:
    def __init__(self):
        self.current_weight = 3000

    def get_weight(self):
        return self.current_weight

    def update_weight(self, amount):
        #print(amount)
        #print(type(amount))
        new_amount = amount[2:-1]
        #print(new_amount)
        self.current_weight = self.current_weight - int(new_amount)


