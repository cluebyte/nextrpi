"""
Modifiers store information that can modify an attribute, and also its origin.
"""


class Modifier(object):

    def __init__(self, desc="unknown", val=0, dbref=None, typeclass=None):
        self.desc = desc
        self.val = val
        self.dbref = dbref
        self.typeclass = typeclass

    def get_modified_val(self, other):
        """Calculate modified value.

        Arguments:
        other (number) - other value to perform calculation with

        Returns: Number
        """
        pass

    def serialize(self):
        """Serialize for storage.

        Arguments: None

        Returns: dict
        """
        return {
                "desc": self.desc,
                "val": self.val,
                "op": self.op,
                "dbref": dbref,
                "typeclass": self.typeclass
        }

    @property
    def op(self):
        return "undefined"

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.serialize())

    def __repr__(self):
        return str(self.serialize())

    def factory(op, **kwargs):
        """Factory method to instantiate the correct Modifier.

        Arguments: None

        Returns: Modifier
        """
        if op == "+":
            return AddModifier(**kwargs)
        if op == "-":
            return SubtractModifier(**kwargs)
        if op == "*":
            return MultiplyModifier(**kwargs)
        if op == "/":
            return DivideModifier(**kwargs)
        assert 0, "Bad Modifier creation: '{}'".format(op)

    factory = staticmethod(factory)


class AddModifier(Modifier):

    def __init__(self, **kwargs):
        super(Modifier, self).__init__(**kwargs)

    def get_modified_val(self, other):
        return other + self.val

    @property
    def op(self):
        return "+"


class SubtractModifier(Modifier):

    def __init__(self, **kwargs):
        super(Modifier, self).__init__(**kwargs)

    def get_modified_val(self, other):
        return other - self.val

    @property
    def op(self):
        return "-"


class MultiplyModifier(Modifier):

    def __init__(self, **kwargs):
        super(Modifier, self).__init__(**kwargs)

    def get_modified_val(self, other):
        return other * self.val

    @property
    def op(self):
        return "*"


class DivideModifier(Modifier):
    def __init__(self, **kwargs):
        super(Modifier, self).__init__(**kwargs)

    def get_modified_val(self, other):
        return other / self.val

    @property
    def op(self):
        return "/"
