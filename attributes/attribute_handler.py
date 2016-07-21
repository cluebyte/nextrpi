"""
AttributeHandler manages the attributes on a character, conveniently storing, 
adding, removing attributes.
"""
from attribute import Attribute, AttributeException
from resource import Resource
from attribute_observer import AttributeObserver
from observer_constants import NotifyType
from evennia.utils.search import search_object


class AttributeHandler(object):
    """
    Properties:
    char_dbref (int) - dbref id of the character observer is attached to
    category (string) - category of the attributes under handler
    attributes (dict) - attribute_name: Attribute mappings of all attributes in
                        handler
    observer (AttributeObserver) - observer that pushes updates to the
                                   Character-level
    """
    def __init__(self, char, category="attributes"):
        self._char_dbref = char.id
        self._category = category
        self.attributes = {}
        self.observer = AttributeObserver(char.id, category)
        # load all attributes into the handler
        self.populate_cache()

    @property
    def category(self):
        return self._category

    @property
    def char_dbref(self):
        return self._char_dbref

    @property
    def character(self):
        """Return the character associated to the char_dbref.
        
        Arguments: None
        Returns: Character
        """
        char = search_object("#{}".format(self.char_dbref))
        if not char:
            raise AttributeException("""character not found 
                                        with id {}""".format(self.char_dbref))
        return char

    def all(self):
        """Gets all attributes in cache.

        Arguments: None
        Returns: List[Attribute]
        """
        return self.attributes.values()

    def get(self, name, default=None):
        """Get an attribute on the character.
        
        Arguments: 
        name (string) - name of the attribute used to store on character
        default (None) - default return value if attribute not found
        """
        # if dict is currently empty, we repopulate the cache before we try
        # and get any attributes
        if not self.attributes:
            self.populate_cache()
        if self.attributes.get(name):
            return self.attributes[name]
        if not default:
            raise AttributeException(
                                "could not find attribute {}".format(name)
            )
        return default

    def add(self, **serialized_attr):
        """Add an attribute to the character.

        Arguments:
        serialized_attr - serialized_attr used to instantiate Attribute
        
        Returns: None
        """
        if self.get(serialized_attr.name):
            raise AttributeException("""attribute {} already 
                                        exists""".format(serialized_attr.name))
        attr = self._build_attribute(**serialized_attr)
        self.attributes[name] = attr
        self.observer.notify_observer()
        self.notify_observer(NotifyType.CREATE, name, attr.serialize())

    def remove(self, name):
        """Remove an attribute from the character.

        Arguments:
        name (string) - name of the attribute

        Returns: None
        """
        if not self.get(name):
            raise AttributeException("could not find attribute {}".format(name))
        del self.attributes[name]
        self.notify_observer(NotifyType.DELETE, name)

    def notify_observer(self, type):
        """Notify the observer that an attribute has been changed.

        Arguments:
        type (NotifyType) - notification type of the change

        Returns: None
        """
        self.observer.notify(type, self.name, self.serialize())

    def clear(self):
        """Clear all attributes from the character.

        Arguments: None
        Returns: None
        """
        for name in self.attributes.keys():
            self.remove(name)

    def _build_attribute(self, **serialized_attr):
        if serialized_attr.type == "attribute":
            return Attribute(self.observer, **serialized_attr)
        elif serialized_attr.type == "resource":
            return Resource(self.observer, **serialized_attr)
        else:
            assert 0, "invalid attribute type: {}".format(serialized_attr.type)

    def _fetch_all(self):
        """Fetch all attributes and build them in our cache.
    
        Arguments: 
        char (Character typeclass) - character we are fetching attributes from

        Returns: None
        """
        # clear the cache
        self.attributes = {}
        attr_dicts = self.character.attributes.get(category=self.category)
        for attr in attr_dicts:
            self.attributes[attr.name] = self._build_attribute(attr)

    def populate_cache(self):
        """Populate the attribute handler cache with all attributes.

        Arguments: None
        Returns: None
        """
        self._fetch_all()

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        if getattr(self, name):
            self.__dict__[name] = value
        else:
            self.add(**value)

    def __len__(self):
        return len(self.attributes.keys())
