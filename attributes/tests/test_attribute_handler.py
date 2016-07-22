"""
Unit test for AttributeHandler.
"""
from django.test import TestCase
from mock import Mock
from attributes.attribute_handler import AttributeHandler
from attributes.attribute import Attribute

def load_cache(func):
    def wrapper(self, *args, **kwargs):
        self.handler.populate_cache()
        func(self, *args, **kwargs)
    return wrapper


class AttributeHandlerTestCase(TestCase):

    DEFAULT_CATEGORY = "attributes"
    ATTR_1 = {
                'name': 'test_attr1',
                'min': -50,
                'base': 5,
                'max': 100,
                'mods': [],
                'type': 'attribute',
    }
    ATTR_2 = {
                'name': 'test_attr2',
                'min': 0,
                'base': 50,
                'max': 200,
                'mods': [],
                'type': 'attribute',
    }
    ATTR_3 = {
                'name': 'test_attr3',
                'min': -100,
                'base': 0,
                'max': 100,
                'mods': [],
                'type': 'attribute',
    }

    RAW_ATTRS = [
                    ATTR_1,
                    ATTR_2,
    ]
    CHAR_DBREF = 1

    def setUp(self):
        mock_obs = Mock()
        char = Mock()
        char.id = self.CHAR_DBREF
        self.attr_1 = Attribute(mock_obs, **self.ATTR_1)
        self.attr_2 = Attribute(mock_obs, **self.ATTR_2)
        self.attr_3 = Attribute(mock_obs, **self.ATTR_3)
        self.handler = AttributeHandler(char)
        self.handler._get_raw_attrs = Mock(return_value=self.RAW_ATTRS)
        self.handler.observer = mock_obs
        self.handler.notify_observer = Mock()

    def tearDown(self):
        self.handler = None

    def test_load_cache(self):
        self.handler.populate_cache()
        self.assertEqual(
                        {
                            self.attr_1.name: self.attr_1,
                            self.attr_2.name: self.attr_2
                        }, 
                        self.handler.attributes)

    @load_cache
    def test_initial_state(self):
        self.assertEqual(self.DEFAULT_CATEGORY, self.handler.category)
        self.assertEqual(
                        {
                            self.attr_1.name: self.attr_1,
                            self.attr_2.name: self.attr_2
                        }, 
                        self.handler.attributes)
        self.assertEqual(self.CHAR_DBREF, self.handler.char_dbref)

    @load_cache
    def test_all(self):
        self.assertEqual([self.attr_1, self.attr_2],
                        self.handler.all())

    @load_cache
    def test_add(self):
        self.handler.add(**self.ATTR_3)
        self.assertIn(self.attr_3.name, self.handler.attributes.keys())
        self.assertIn(self.attr_3, self.handler.attributes.values())

    @load_cache
    def test_remove(self):
        self.handler.remove(self.ATTR_2['name'])
        self.assertNotIn(self.attr_2.name, self.handler.attributes.keys())
        self.assertNotIn(self.attr_2, self.handler.attributes.values())

    @load_cache
    def test_get(self):
        self.assertEqual(self.handler.get(self.ATTR_2['name']), self.attr_2)

    @load_cache
    def test_get_as_property(self):
        self.assertEqual(self.handler.test_attr2, self.attr_2)
