"""
Delay Handlers should be initialized once on every Object that you care to
keep track of delays on.

Delay Handlers validate delays and remove any inactive delays, as well as
retrieve any delays currently on a character. Delay Handlers also ensure that
any delays are recreated on server restart and reload so that delays persist
across server restart/reloads.
"""

from delay import Delay


class DelayHandlerException(Exception):
    def __init__(self, msg):
        super(DelayHandlerException, self).__init__(msg)


class DelayHandler(object):

    def __init__(self, attrobj):
        """
        Arguments:
        attrobj (Evennia Attribute obj ref) - reference to the Evennia Attribute
                                              object that we use to persist
                                              delays across reload/restarts
        """
        self.delays = {}
        self.attrobj = attrobj

    def add(self, name, **kwargs):
        """Add a delay with the specified name and constructor kwargs.

        Arguments:
        name (string) - name of the delay
        kwargs (dict) - constructor args for Delay
        """
        if not self.delays.get(name, None):
            raise DelayHandlerException("delay with name: {} already exists, "
                                        "add failed".format(name))
        self.delays[name] = Delay(**kwargs)

    def get(self, name, default=None):
        """Get a delay with the specified name.

        Arguments:
        name (string) - name of the delay
        default (any or None) - default that should be returned if delay isn't
                                found

        Returns: Delay
        """
        if default:
            return self.delays.get(name, default)
        res = self.delays.get(name)
        if not res:
            raise DelayHandlerException("delay with name: {} doesn't exist, "
                                        "get failed".format(name))
        return res

    def remove(self, name):
        """Remove a delay registered with the specified name.

        Arguments:
        name (string) - name of the delay

        Returns: None
        """
        try:
            del self.delays[name]
        except KeyError:
            raise DelayHandlerException("delay with name: {} doesn't exist, "
                                        "removal failed".format(name))

    def all(self):
        """Return a dict representation of all delays.

        Arguments: None

        Returns: dict (string: Delay)
        """
        return dict(self.delays)

    def _serialize(self):
        """Save current delays in a serialized format.

        Arguments: None

        Returns: dict (string: dict of delay constructor args)
        """
        serialized = {}
        for name, delay in self.delays.iteritems():
            serialized[name] = delay.serialize()
        return serialized

    def save(self):
        """Save all the delays on the handler to the Evennia Attribute reference.

        Arguments: None

        Returns: None
        """
        self.validate()
        serialized = self._serialize()
        self.attrobj.value = serialized

    def clear(self):
        """Remove all delays on the handler to the Evennia Attribute reference.

        Arguments: None

        Returns: None
        """
        for name, delay in self.delays.iteritems():
            self.remove(name)
        self.save()

    def validate(self):
        """Clean up any delays that are inactive from the handler.

        Arguments: None

        Returns: None
        """
        for name, delay in self.delays.iteritems():
            if not delay.is_active():
                del self.delays[name]

    def load_delays(self):
        """Load all serialized delays on the handler.

        Arguments: None

        Returns: None
        """
        serialized = self.attrobj.value
        for name, kwargs in serialized:
            self.delays[name] = Delay(**kwargs)
