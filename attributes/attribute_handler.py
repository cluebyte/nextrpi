"""
AttributeHandler manages the attributes on a character, conveniently storing, 
adding, removing attributes.
"""
from attribute import Attribute, AttributeException
from resource import Resource
from attribute_observer import AttributeObserver
from observer_constants import NotifyType
from evennia.utils.search import search_object
from evennia.utils.utils import lazy_property


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
        self._attributes = {}
        self._loaded = False

    @lazy_property
    def observer(self):
        return AttributeObserver(char.id, category)

    @property
    def attributes(self):
        if not self._loaded:
            self.populate_cache()
            self._loaded = True
        return self._attributes
        
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

    def get(self, name, **kwargs):
        """Get an attribute on the character.
        
        Arguments: 
        name (string) - name of the attribute used to store on character
        default (None) - default return value if attribute not found
        """
        # if dict is currently empty, we repopulate the cache before we try
        # and get any attributes
        if self.attributes.get(name):
            return self.attributes[name]
        if 'default' in kwargs:
            return kwargs.get('default')
        raise AttributeException(
                                "could not find attribute {}".format(name))

    def add(self, **serialized_attr):
        """Add an attribute to the character.

        Arguments:
        serialized_attr - serialized_attr used to instantiate Attribute
        
        Returns: None
        """
        name = serialized_attr.get('name')
        if self.get(name, default=None):
            raise AttributeException("""attribute {} already 
                                        exists""".format(name))
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

    def _clear_cache(self):
        """Clear the cache of attributes.

        Arguments: None
        Returns: None
        """
        self._attributes = {}

    def _build_attribute(self, **serialized_attr):
        if serialized_attr.get('type') == "attribute":
            return Attribute(self.observer, **serialized_attr)
        elif serialized_attr.get('type') == "resource":
            return Resource(self.observer, **serialized_attr)
        else:
            assert 0, """invalid
                        attribute type: {}""".format(
                                            serialized_attr.get('type'))

    def _get_raw_attrs(self):
        """Get all raw attributes in serialized format from the character.

        Arguments: None
        Returns: List[dict]
        """
        return self.character.attributes.get(category=self.category)

    def _fetch_all(self):
        """Fetch all attributes and build them in our cache.
    
        Arguments: 
        char (Character typeclass) - character we are fetching attributes from

        Returns: None
        """
        # clear the cache
        self._clear_cache()
        attr_dicts = self._get_raw_attrs()
        for attr in attr_dicts:
            self._attributes[attr['name']] = self._build_attribute(**attr)

    def populate_cache(self):
        """Populate the attribute handler cache with all attributes.

        Arguments: None
        Returns: None
        """
        self._fetch_all()

    def __getattr__(self, name):
        return self.get(name)

    def __len__(self):
        return len(self.attributes.keys())
