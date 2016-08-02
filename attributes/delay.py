"""
Delays act as a wrapper on the Twisted Deferred object that is returned from
Evennia's delay utility function. Delays act as callbacks in NextRPI, which
allows various applications, such as enforcing cooldowns, and simulating
regenerating resources.
"""

from evennia.utils.utils import delay
import time


class Delay(object):
    """
    Properties:
    deferred (Deferred) - a Twisted deferred object that contains information about
                          the callback (if any)
    """
    def __init__(self, delay_in_seconds, callback=None, retval=None):
        """
        Arguments:
        delay_in_seconds (int or float) - delay until callback is fired
        callback (func) - callback to call, if any, after delay elapses
        retval (any, or None) - any arguments to return or input to
                                to callback
        """
        if retval:
            self.deferred = delay(delay_in_seconds, callback, retval)
        else:
            self.deferred = delay(delay_in_seconds, callback)

    @property
    def callback(self):
        return self.deferred.func

    @property
    def retval(self):
        return self.deferred.args

    def delay_more(self, seconds):
        """Delay the callback by additional seconds.

        Arguments:
        seconds (int) - seconds to additionally delay the callback
        """
        self.deferred.delay(seconds)

    def reset(self, seconds_from_now):
        """Reset the callback and then delay by specified seconds.

        Arguments:
        seconds_from_now (int or float) - new delay in seconds before firing callback
        """
        self.deferred.reset(seconds_from_now)

    def is_active(self):
        """Return True if callback is still active or False if already called.

        Arguments: None

        Returns: boolean
        """
        return self.deferred.active()

    def cancel(self):
        """Cancel the callback.

        Arguments: None

        Returns: None
        """
        self.deferred.cancel()

    def get_time(self):
        """Get time in seconds from epoch of when callback will fire.

        Arguments: None

        Returns: int
        """
        return self.deferred.getTime()

    def get_time_remaining(self):
        """Get seconds remaining until callback is fired.

        Arguments: None

        Returns: float
        """
        return self.get_time() - time.time()
