"""
Attribute Observer uses the Observer Design pattern to push updates up to the character-level for storage.
"""

from evennia.utils.search import search_object
from observer_constants import NotifyType


class ObserverException(Error):
    def __init__(self, msg):
        super(ObserverException, self).__init__(msg)
        self.msg = msg


class AttributeObserver(object):

    def __init__(self, dbref, category):
        self.char_dbref = dbref
        self.category = category

    def notify(self, type, **kwargs):
        """Notify the observer to push updates to the character.

        Arguments:
        type (NotifyType) - the kind of update to perform
        kwargs - additional arguments for the update

        Returns: None
        """
        if type == NotifyType.UPDATE:
            self._update(**kwargs)
        elif type == NotifyType.DELETE:
            self._deletion(**kwargs)
        elif type == NotifyType.CREATE:
            self._create(**kwargs)
        raise ObserverException("incorrect notify type: {}".format(type))

    @property
    def character(self):
        char = search_object("#{}".format(self.char_dbref))
        if not char:
            raise AttributeError("""character not found 
                                    with id {}""".format(self.char_dbref))
        return char

    def _delete(self, attr_name):
        """Delete attribute from character.

        Arguments:
        attr_name (string) - attribute name stored on character

        Returns: None
        """
        self.character.attributes.remove(attr_name)

    def _update(self, attr_name, serialized_data):
        """Update attribute on character using serialized data.

        Arguments:
        attr_name (string) - attribute name stored on character
        serialized_data (dict) - serialized dict representation of attribute

        Returns: None
        """
        self.character.attributes.remove(attr_name)
        self.character.attributes.add(attr_name, serialized_data, 
                                    category=self.category)

    def _create(self, attr_name, serialized_data):
        """Create attribute on character using serialized_data.

        Arguments:
        attr_name (string) - attribute name stored on character
        serialized_data (dict) - serialized dict representation of attribute

        Returns: None
        """
        self.character.attributes.add(attr_name, serialized_data,
                                    category=self.category)
