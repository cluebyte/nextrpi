"""
Resources represent attributes that can be used or consumed as a resource, such
as health, mana, rocket power, etc.
"""
from attribute import Attribute
from resource_constants import AttributeType
from save_wrapper import save_attr


class Resource(object):
    """
    Properties:
    name (string) - name of the attribute
    min (Attribute) - attribute value floor
    max (Attribute) - attribute value ceiling
    recharge_interval (number) - interval between recharges in seconds
    recharge_rate (number) - how much to increase the current value by, for
                             each recharge interval
    will_charge (boolean) - if recharging is enabled
    cur_val (number) - current value of the resource
    attrobj (Attribute objref) - Evennia database attribute direct object
                                 reference, used to save changes to the handler
    """
    def __init__(self, attrobj, name="resource", cur_val=0, min=None, 
                max=None, recharge_interval=60, recharge_rate=1):
        self.name = name
        self._cur_val = cur_val
        self._min = Attribute(attrobj, **min)
        self._max = Attribute(attrobj, **max)
        self.recharge_rate = recharge_rate
        self.recharge_interval = recharge_interval
        self.will_recharge = False
        self.attrobj = attrobj

    @property
    def max_modifiers(self):
        return self._max.modifiers

    @property
    def min_modifiers(self):
        return self._min.modifiers

    @property
    def max(self):
        return self._max.cur_val

    @property
    def min(self):
        return self._min.cur_val

    @property
    def percentage(self):
      return self.cur_val / self.max

    @property
    def cur_val(self):
        return self._cur_val

    @cur_val.setter
    def cur_val(self, other):
        if other > self.max.cur_val:
            self._cur_val = self.max
        elif other < self.min.cur_val:
            self._cur_val = self.min
        else:
            self._cur_val = other

    def get_mod(self, attr_type, desc, **kwargs):
        """Get modifier based on attribute type, description, and filters.

        Arguments:
        attr_type (AttributeType) - what type of attribute we are adding
                                    modifier to
        desc (string) - name of the modifier
        kwargs (dict) - any filters we want to filter the result by

        Returns: Modifier
        """
        if attr_type == AttributeType.MAX:
            return self.max_modifiers.get(desc, **kwargs)
        if attr_type == AttributeType.MIN:
            return self.min_modifiers.get(desc, **kwargs)
        assert 0, "invalid attr_type {}".format(attr_type)

    @save_attr
    def add_mod(self, attr_type, **kwargs):
        """Add a modifier to the resource's min, or max, based on attr type.

        Arguments:
        attr_type (string) - what type of attribute we are adding modifier to
        kwargs - filter arguments used to grab modifier

        Returns: None
        """
        if attr_type == AttributeType.MAX:
            self.max_modifiers.add(**kwargs)
        elif attr_type == AttributeType.MIN:
            self.min_modifiers.add(**kwargs)
        else:
            assert 0, "invalid attr_type {}".format(attr_type)

    @save_attr
    def remove_mod(self, attr_type, modifier):
        """Remove a modifier from the resource min/max based on attr_type.

        Arguments:
        attr_type (string) - what type of attribute we are adding modifier to
        modifier (Modifier) - modifier to remove

        Returns: None
        """
        if attr_type == AttributeType.MAX:
            self.max_modifiers.remove(modifier)
        elif attr_type == AttributeType.MIN:
            self.min_modifiers.remove(modifier)
        else:
            assert 0, "invalid attr_type {}".format(attr_type)

    def serialize(self):
        """Serialize for storage.

        Arguments: None

        Returns: dict
        """
        return {
                "min": self._min.serialize(),
                "max": self._max.serialize(),
                "will_recharge": self.will_recharge,
                "cur_val": self.cur_val,
                "recharge_rate": self.recharge_rate,
                "recharge_interval": self.recharge_interval
        }

    @save_attr
    def restore(self):
        """Restore resource to the max.
        
        Arguments: None

        Returns: None
        """
        self.cur_val = self.max

    @save_attr
    def deplete(self):
        """Deplete resource to the minimum.
        
        Arguments: None

        Returns: None
        """
        self.cur_val = self.min

    @save_attr
    def recharge(self):
        """Recharge the resource by the recharge rate.

        Arguments: None

        Returns: None
        """
        self.cur += self.recharge_rate

    @save_attr
    def toggle_recharge_on(self):
        """Enable recharging for this resource.

        Arguments: None

        Returns: None
        """
        self.will_recharge = True

    @save_attr
    def toggle_recharge_off(self):
        """Disable recharging for this resource.

        Arguments: None

        Returns: None
        """
        self.will_recharge = False
