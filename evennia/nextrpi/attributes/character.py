from typeclasses.characters import Character


class AttributeCharacterMixin(Character):
    """
    Installs Attributes-specific plugins.
    """
    def get_attribute(self, name):
        return self.scripts.get("attribute_%s".format(name))