from attribute import Attribute


class Resource(Attribute):

    def __init__(self, base=0, min=0, max=0, recharge_interval, recharge_rate):
        super(Attribute, self).__init__(base, min, max)
        self.recharge_rate = recharge_rate
        self.recharge_interval = recharge_interval
        self.will_recharge = False

    def restore(self):
        self.cur_val = self.max

    def deplete(self):
        self.cur_val = self.min

    def toggle_recharge(self):
        self.will_recharge = not self.will_recharge
