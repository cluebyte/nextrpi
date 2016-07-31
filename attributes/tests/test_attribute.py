"""
Unit test module for Attribute classes.
"""
from django.test import TestCase
from attributes.attribute import Attribute
from mock import Mock


class AttributeTestCase(TestCase):

    MOD_VAL = -10
    BASE_VAL = 20
    MIN_VAL = 0
    MAX_VAL = 100

    def setUp(self):
        self.attr = Attribute(Mock(), name="test_attr", base=self.BASE_VAL,
                              min=self.MIN_VAL, max=self.MAX_VAL)
        self.attr._get_modified_val = Mock(return_value=self.MOD_VAL)
        self.attr._get_serialized_mods = Mock(return_value=[])

    def tearDown(self):
        self.attr = None

    def test_initial_state(self):
        self.assertEqual(self.attr.name, "test_attr")
        self.assertEqual(self.attr.base, self.BASE_VAL)
        self.assertEqual(self.attr.min, self.MIN_VAL)
        self.assertEqual(self.attr.max, self.MAX_VAL)
        self.assertEqual(self.attr.cur_val, self.BASE_VAL + self.MOD_VAL)

    def test_modify_base(self):
        self.attr.base += 1
        self.assertEqual(self.attr.base, self.BASE_VAL + 1)

    def test_modify_base_beyond_max(self):
        self.attr.base += 100
        self.assertEqual(self.attr.base, self.attr.max)

    def test_modify_base_below_min(self):
        self.attr.base -= 100
        self.assertEqual(self.attr.base, self.attr.min)

    def test_serialize(self):
        self.assertEqual(self.attr.serialize(), {
                                                  'name': "test_attr",
                                                  'base': 20,
                                                  'min': 0,
                                                  'max': 100,
                                                  'type': 'attribute',
                                                  'modifiers': [] })
