"""
ResourceHandler manages the resources on a character, conveniently storing,
adding, removing resources.
"""
from resource import Resource
from save_wrapper import save_attr


class ResourceHandler(object):
    """
    Properties:
    resources (dict) - resource_name: Resource mappings of all attributes in
                        handler
    attrobj (Attribute objref) - Evennia database attribute direct object
                                 reference, used to save changes to the handler
    """

    def __init__(self):
        self.resources = {}

    def all(self):
        """Gets all resources in cache.

        Arguments: None

        Returns: List[Resource]
        """
        return self.resources.values()

    def get(self, name, **kwargs):
        """Get an resource on the character.

        Arguments:
        name (string) - name of the resource used to store on character
        default (None) - default return value if resource not found

        Returns: Resource
        """
        if self.resources.get(name):
            return self.resources[name]
        if 'default' in kwargs:
            return kwargs.get('default')
        raise AttributeError("could not find resource {}".format(name))

    @save_attr
    def add(self, **serialized_res):
        """Add an resource to the character.

        Arguments:
        serialized_res - serialized_res used to instantiate Attribute

        Returns: None
        """
        name = serialized_res.get('name')
        if self.get(name, default=None):
            raise AttributeError("resource {} already exists".format(name))
        attr = self._build_resource(**serialized_res)
        self.resources[name] = attr

    @save_attr
    def remove(self, name):
        """Remove an resource from the character.

        Arguments:
        name (string) - name of the resource

        Returns: None
        """
        if not self.get(name):
            raise AttributeError("could not find resource {}".format(name))
        del self.resources[name]

    def clear(self):
        """Clear all resources from the character.

        Arguments: None

        Returns: None
        """
        for name in self.resources.keys():
            self.remove(name)

    def _build_resource(self, **serialized_attr):
        """Return built resource given resource serialization.

        Arguments:
        serialized_attr (dict) - serialized resource

        Returns: Attribute or Resource
        """
        return Resource(self.attrobj, **serialized_attr)

    def __getattr__(self, name):
        return self.get(name)

    def __len__(self):
        return len(self.resources.keys())

    def __repr__(self):
        return str(self.__dict__)
