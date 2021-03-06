"""
ModifierHandler manages the modifiers on a given attribute, conveniently storing, adding, removing, and calculating the final modified result based on all the modifiers stored.
"""
from modifier import Modifier


class ModifierHandler(object):

    def __init__(self, raw_modifiers):
        self.modifiers = {}
        self._raw_modifiers = []

        for raw_mod in raw_modifiers:
            self.add(**raw_mod)

    def add(self, **raw_mod):
        """Add a modifier to the modifier handler. 

        Arguments:
        raw_mod (kwargs) - constructor arguments for Modifier

        Returns: None
        """
        mod_desc = raw_mod["desc"]
        if not self.modifiers.get(mod_desc):
            self.modifiers[mod_desc] = []
        new_mod = Modifier.factory(**raw_mod)
        self.modifiers[mod_desc].append(new_mod)
        self._raw_modifiers.append(new_mod)

    def remove(self, modifier):
        """Remove a modifier to the modifier handler.

        Arguments:
        modifier (Modifier) - Modifier instance to be removed

        Returns: None
        """
        try:
            self._raw_modifiers.remove(modifier)
        except:
            raise AttributeError("could not find modifier {}".format(modifier))
        mod_desc = modifier.desc
        for mod in self.modifiers[mod_desc]:
            if modifier == mod:
                self.modifiers[mod_desc].remove(modifier)
                return

    def get(self, desc, **filters):
        """Get a modifier matching the desc and any additional filters.

        This will return the first candidate that matches the desc and all
        additional filters. Additional filters will attempt to match
        modifier.filter_key == filter_val.

        Arguments:
        desc (string) - description of modifier
        filters (kwargs) - filters by modifier attribute

        Returns: Modifier

        Example: self.get("caffeine addiction", dbref=3, typeclass="Medicine")
        """
        found = True
        for candidate in self.modifiers[desc]:
            for filter_attr, filter_val in filters.items():
                if getattr(candidate, filter_attr) != filter_val:
                    found = False
            if found:
                return candidate
            found = True
        raise AttributeError("can't find modifier {}".format(desc))

    def all(self):
        """Fetch all modifiers that exist on the attribute.
        
        Arguments: None

        Returns: List[Modifier]
        """
        return list(self._raw_modifiers)

    def get_modified_val(self, base_val):
        """Get the calculated modified value based on existing modifiers.

        Arguments:
        base_val (number) - base value to modify

        Returns: Number
        """
        mods = self.all()
        res = self._resolve_modified_val(base_val)
        return res

    def _resolve_modified_val(self, base_val):
        """Resolve order of operations for modifier parameters.

        Return the modified value based on order of operations of the modifiers.

        Arguments:
        base_val (number) - base value we are modifying

        Returns: Number
        """
        modifiers = self.all()
        mul_div_ops = [mod for mod in modifiers if mod.operator in ["*","/"]]
        add_sub_ops = [mod for mod in modifiers if mod.operator in ["+", "-"]]
        res = base_val
        for mod in mul_div_ops:
            res = mod.get_modified_val(res)
        for mod in add_sub_ops:
            res = mod.get_modified_val(res)
        return res

    def serialize_all_mods(self):
        """Serialize all modifiers for storage.

        Arguments: None

        Returns: List[dict]
        """
        mods = self.all()
        return [
                mod.serialize() for mod in mods]

    def __len__(self):
        return len(self._raw_modifiers)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
