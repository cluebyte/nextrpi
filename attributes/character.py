from typeclasses.objects import Object


class AttributeCharacterMixin(Object):
    """
    Installs Attributes-specific plugins.
    """
    def get_attribute(self, name):
        return self.scripts.get("attribute_{0}".format(name))[0]