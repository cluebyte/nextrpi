class Modifier(object):

    def __init__(self, val, origin="unknown source"):
        self.val = val
        self.origin = origin

    def get_modified_val(self, other):
        pass

class AddModifier(Modifier):

    def __init__(self, val, origin="unknown source"):
        super(Modifier, self).__init__(val, origin)

    def get_modified_val(self, other):
        return other + self.val


class SubtractModifier(Modifier):

    def __init__(self, val, origin="unknown source"):
        super(Modifier, self).__init__(val, origin)

    def get_modified_val(self, other):
        return other - self.val


class MultiplyModifier(Modifier):

    def __init__(self, val, origin="unknown source"):
        super(Modifier, self).__init__(val, origin)

    def get_modified_val(self, other):
        return other * self.val
