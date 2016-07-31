"""
Save wrapper for attribute objects. This will save any changes made to custom
Python objects to Evennia typeclasses by using the AttributeHandler.

If you intend on using this wrapper, your Object MUST have an 'attrobj'
member variable on it that contains the attribute object reference to the
Evennia database attribute. For example, you can grab this by using:

your_evennia_obj.attributes.get("something", return_obj=True)

Example:

class Mystery(object):
    def __init__(self):
        self.attrobj = None
        self.data = None

    # note the decorator goes here, and will save AFTER the function call is
    # done
    @save_attr
    def add(self, data):
        self.data = data

import evennia 
from world.test import Mystery

obj = evennia.search_object("MyObject")[0]

# preparing the Attribute 

obj.db.mystery = Mystery()
# We must use the AttributeHandler to get the Attribute object 
# itself instead of just its value
obj.db.mystery.attrobj = obj.attributes.get("mystery", return_obj=True)

# testing to use it 

obj.db.mystery.add("Foo")
obj.db.mystery.data   # this is now "Foo"

# Now restart and load everything up again

obj.db.mystery.data  # this is still "Foo"

Credits for this example goes to Griatch Art from the Evennia Google Group,
originally found here:

https://groups.google.com/forum/#!category-topic/evennia/evennia-questions/fI0pQTpvGkA
"""

def save_attr(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        def save(self):
            self.attrobj.value = self
        save(self)
    return wrapper
