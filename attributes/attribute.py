"""
Attributes represent a character attribute of some sort, such as strength,
health These attributes can be modified by Modifiers. Attributes are typically 
used to calculate character growth and affect outcomes, such as dealing more 
damage, making an athletics check to vault over a wall, etc.
"""
from modifier_handler import ModifierHandler
from observer_constants import NotifyType
from evennia.utils.utils import lazy_property
from save_wrapper import save_attr


class AttributeException(Exception):
    def __init__(self, msg):
        super(AttributeException, self).__init__(msg)
        self.msg = msg


class Attribute(object):
    """
    Properties:
    name (string) - name of the attribute
    base (number) - the value the attribute starts at
    min (number) - attribute value floor
    max (number) - attribute value ceiling
    modifiers (ModifierHandler) - stores all the modifiers
    attrobj (Attribute objref) - Evennia database attribute direct object
                                 reference, used to save changes to the handler
    """
    def __init__(self, attrobj, **kwargs):
        self._name = kwargs.get('name')
        self._base = kwargs.get('base')
        self.min = kwargs.get('min')
        self.max = kwargs.get('max')
        self.modifiers = ModifierHandler(self._raw_mods)
        self.attrobj = attrobj

    @property
    def name(self):
        return self._name

    @property
    def cur_val(self):
        mod_val = self._get_modified_val(self.base)
        cur_val = self.base + mod_val
        return self._check_bounds(cur_val)

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, new_val):
        new_val = self._check_bounds(new_val)
        self._base = new_val

    def _get_modified_val(self):
        """Get the sum of the modifiers on the attribute.

        Arguments: None
        Returns: Number
        """
        return self.modifiers.get_modified_val(self.base)

    def _check_bounds(self, val):
        """Check if the value exceeds the ceiling or floor of attribute value.

        If it exceeds the bounds, we return the max or min. Or else we return
        the value passed in.

        Arguments:
        val (number) - value that we are checking the bounds for

        Returns: Number
        """
        if val > self.max:
            return self.max
        elif val < self.min:
            return self.min
        else:
            return val

    def get_mod(self, desc, **kwargs):
        """Get a modifier from the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: Modifier
        """
        return self.modifiers.get(desc, **kwargs)

    @save_attr
    def add_mod(self, **kwargs):
        """Add a modifier to the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: None
        """
        self.modifiers.add(**kwargs)

    @save_attr
    def remove_mod(self, modifier):
        """Remove a modifier from the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: None
        """
        self.modifiers.remove(modifier)

    def _get_serialized_mods(self):
        """Fetch all serialized modifiers attached on the attribute.

        Arguments: None
        Returns: List[dict]
        """
        return self.modifiers.serialize_all_mods()

    def serialize(self):
        """Serialize for storage.

        Arguments: None

        Returns: dict
        """
        return {
                "name": self.name,
                "base": self.base,
                "min": self.min,
                "max": self.max,
                "type": "attribute",
                "modifiers": self._get_serialized_mods() }

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.serialize())

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
