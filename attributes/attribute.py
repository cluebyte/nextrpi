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
    modifier_handler (ModifierHandler) - stores all the modifiers
    observer (AttributeObserver) - stores the observer that pushes updates
                                    to the Character-level
    """
    def __init__(self, observer, name="attr", base=0, min=0, max=0, mods=None):
        self._name = name
        self._base = base
        self.min = min
        self.max = max
        self.modifier_handler = ModifierHandler(mods)
        self.observer = observer

    @property
    def name(self):
        return self._name

    @property
    def cur_val(self):
        mod_val = self.modifier_handler.get_modified_val(self.base)
        return self.base + mod_val

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, new_val):
        if new_val > self.max:
            self._base = self.max
        elif new_val < self.min:
            self._base = self.min
        else:
            self._base = new_val

    def notify_observer(self, type):
        """Notify the observer that an attribute has been changed.

        Arguments:
        type (NotifyType) - notification type of the change

        Returns: None
        """
        self.observer.notify(type, self.name, self.serialize())

    def get_mod(source, **kwargs):
        """Get a modifier from the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: Modifier
        """
        return self.modifier_handler.get(**kwargs)

    def add_mod(**kwargs):
        """Add a modifier to the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: None
        """
        self.modifier_handler.add(**kwargs)
        self.notify_observer(NotifyType.UPDATE)

    def remove_mod(self, modifier):
        """Remove a modifier from the attribute.

        Arguments:
        kwargs - filter arguments used to grab modifier

        Returns: None
        """
        self.modifier_handler.remove(modifier)
        self.notify_observer(NotifyType.DELETE)

    def serialize(self):
        """Serialize for storage.

        Arguments: None

        Returns: dict
        """
        return {
                "base": self.base,
                "min": self.min,
                "max": self.max,
                "modifiers": self.modifier_handler.serialize_all_mods()
        }

    def __repr__(self):
        return self.serialize()

    def __str__(self):
        return self.serialize()
