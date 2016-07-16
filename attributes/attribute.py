"""
Attributes represent a character attribute of some sort, such as strength,
health These attributes can be modified by Modifiers. Attributes are typically 
used to calculate character growth and affect outcomes, such as dealing more 
damage, making an athletics check to vault over a wall, etc.
"""
from modifier_handler import ModifierHandler
from observer_constants import NotifyType


class Attribute(object):
    """
    Attributes:
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
        self.modifiers = ModifierHandler(mods)
        self.observer = observer

    @property
    def name(self):
        return self._name

    @property
    def cur_val(self):
        mod_val = self.modifiers.get_modified_val(self.base)
        cur_val = self.base + mod_val
        return self._check_bounds(cur_val)

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, new_val):
        new_val = self._check_bounds(new_val)
        self._base = new_val

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

    def get_mod(desc, **kwargs):
        """Get a modifier from the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: Modifier
        """
        return self.modifiers.get(desc, **kwargs)

    def add_mod(**kwargs):
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

    def serialize(self):
        """Serialize for storage.

        Arguments: None

        Returns: dict
        """
        return {
                "base": self.base,
                "min": self.min,
                "max": self.max,
                "modifiers": self.modifiers.serialize_all_mods()
        }

    def __repr__(self):
        return self.serialize()

    def __str__(self):
        return self.serialize()
