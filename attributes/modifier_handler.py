class ModifierHandler(object):

    def __init__(self):
        self.modifiers = []

    def add(self, modifier):
        self.modifiers.append(modifier)

    def remove(self, modifier):
        self.modifiers.remove(modifier)

    def get_modified_val(self):
        pass

    def get_itemized_list(self):
        pass
