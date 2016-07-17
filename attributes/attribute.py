"""
Attributes represent a character attribute of some sort, such as strength,
health These attributes can be modified by Modifiers. Attributes are typically 
used to calculate character growth and affect outcomes, such as dealing more 
damage, making an athletics check to vault over a wall, etc.
"""
from modifier_handler import ModifierHandler
from observer_constants import NotifyType
from evennia.utils.utils import lazy_property


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
    observer (AttributeObserver) - observer that pushes updates to the
                                   Character-level
    """
    def __init__(self, observer, name="attr", base=0, min=0, max=0, mods=None):
        self._name = name
        self._base = base
        self.min = min
        self.max = max
        self._raw_mods = mods if mods else []
        self.observer = observer

    @lazy_property
    def modifiers(self):
        return ModifierHandler(self._raw_mods)

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

    def notify_observer(self, type):
        """Notify the observer that an attribute has been changed.

        Arguments:
        type (NotifyType) - notification type of the change

        Returns: None
        """
        self.observer.notify(type, self.name, self.serialize())

    def get_mod(self, desc, **kwargs):
        """Get a modifier from the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: Modifier
        """
        return self.modifiers.get(desc, **kwargs)

    def add_mod(self, **kwargs):
        """Add a modifier to the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: None
        """
        self.modifiers.add(**kwargs)
        self.notify_observer(NotifyType.UPDATE)

    def remove_mod(self, modifier):
        """Remove a modifier from the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: None
        """
        self.modifiers.remove(modifier)
        self.notify_observer(NotifyType.UPDATE)

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
        return self.serialize()

    def __str__(self):
        return self.serialize()
