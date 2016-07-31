"""
Unit test for AttributeHandler.
"""
from django.test import TestCase
from mock import Mock
from attributes.attribute_handler import AttributeHandler
from attributes.attribute import Attribute


class AttributeHandlerTestCase(TestCase):

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

    def setUp(self):
        char = Mock()
        self.handler = AttributeHandler(char)
        self.handler.attrobj = Mock()
        self.attr_1 = Attribute(self.handler.attrobj, **self.ATTR_1)
        self.attr_2 = Attribute(self.handler.attrobj, **self.ATTR_2)
        self.attr_3 = Attribute(self.handler.attrobj, **self.ATTR_3)
        self.handler.attributes = {
                                    self.attr_1.name: self.attr_1,
                                    self.attr_2.name: self.attr_2 }

    def tearDown(self):
        self.handler = None

    def test_initial_state(self):
        self.assertEqual(
                        {
                            self.attr_1.name: self.attr_1,
                            self.attr_2.name: self.attr_2
                        }, 
                        self.handler.attributes)

    def test_all(self):
        self.assertEqual([self.attr_1, self.attr_2],
                        self.handler.all())

    def test_add(self):
        self.handler.add(**self.ATTR_3)
        self.assertIn(self.attr_3.name, self.handler.attributes.keys())
        self.assertIn(self.attr_3, self.handler.attributes.values())

    def test_remove(self):
        self.handler.remove(self.ATTR_2['name'])
        self.assertNotIn(self.attr_2.name, self.handler.attributes.keys())
        self.assertNotIn(self.attr_2, self.handler.attributes.values())

    def test_get(self):
        self.assertEqual(self.handler.get(self.ATTR_2['name']), self.attr_2)

    def test_get_as_property(self):
        self.assertEqual(self.handler.test_attr2, self.attr_2)
