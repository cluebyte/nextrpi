"""
AttributeHandler manages the attributes on a character, conveniently storing, 
adding, removing attributes.
"""
from attribute import Attribute
from save_wrapper import save_attr


class AttributeHandler(object):
    """
    Properties:
    attributes (dict) - attribute_name: Attribute mappings of all attributes in
                        handler
    attrobj (Attribute objref) - Evennia database attribute direct object
                                 reference, used to save changes to the handler
    """
    def __init__(self):
        self.attributes = {}

    def all(self):
        """Gets all attributes in cache.

        Arguments: None

        Returns: List[Attribute]
        """
        return self.attributes.values()

    def get(self, name, **kwargs):
        """Get an attribute on the character.
        
        Arguments: 
        name (string) - name of the attribute used to store on character

        default (None) - default return value if attribute not found
        """
        if self.attributes.get(name):
            return self.attributes[name]
        if 'default' in kwargs:
            return kwargs.get('default')
        raise AttributeError("could not find attribute {}".format(name))

    @save_attr
    def add(self, **serialized_attr):
        """Add an attribute to the character.

        Arguments:
        serialized_attr - serialized_attr used to instantiate Attribute
        
        Returns: None
        """
        name = serialized_attr.get('name')
        if self.get(name, default=None):
            raise AttributeError("attribute {} already exists".format(name))
        attr = self._build_attribute(**serialized_attr)
        self.attributes[name] = attr

    @save_attr
    def remove(self, name):
        """Remove an attribute from the character.

        Arguments:
        name (string) - name of the attribute

        Returns: None
        """
        if not self.get(name):
            raise AttributeError("could not find attribute {}".format(name))
        del self.attributes[name]

    def clear(self):
        """Clear all attributes from the character.

        Arguments: None

        Returns: None
        """
        for name in self.attributes.keys():
            self.remove(name)

    def _build_attribute(self, **serialized_attr):
        """Return built attribute given attribute serialization.

        Arguments: 
        serialized_attr (dict) - serialized attribute

        Returns: Attribute or Resource
        """
        return Attribute(self.attrobj, **serialized_attr)

    def __getattr__(self, name):
        return self.get(name)

    def __len__(self):
        return len(self.attributes.keys())

    def __repr__(self):
        return str(self.__dict__)
