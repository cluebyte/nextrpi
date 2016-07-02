"""
Attributes represent a character attribute of some sort, such as strength,
health, or a skill, usually represented by a number. These attributes can
be modified by Modifiers. Attributes are typically used to calculate character
growth and affect outcomes, such as dealing more damage, making an athletics
check to vault over a wall, etc.
"""

from modifier_handler import ModifierHandler


class Attribute(object):

    def __init__(self, base=0, min=0, max=0):
        self._base = base
        self.min = min
        self.max = max
        self.modifier_handler = ModifierHandler()

    @property
    def cur_val(self):
        mod_val = self.modifier_handler.get_modified_val()
        return self.base + mod_val

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, new_val):
        if new_val > self.max:
            self.base = self.max
        elif new_val < self.min:
            self.base = self.min
        else:
            self.base = new_val

    def add_modifier(self, modifier):
        self.modifier_handler.add(modifier)

    def remove_modifier(self, modifier):
        self.modifier_handler.remove(modifier)
