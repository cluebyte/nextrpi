"""
Unit test module for Attribute classes.
"""
from django.test import TestCase
from attributes.attribute import Attribute
from attributes.modifier_handler import ModifierHandler
from mock import Mock
from attributes.attribute_observer import AttributeObserver


class AttributeTestCase(TestCase):

    MOD_VAL = -10
    BASE_VAL = 20
    MIN_VAL = 0
    MAX_VAL = 100

    def setUp(self):
        obs_mock = Mock(spec=AttributeObserver)
        self.attr = Attribute(obs_mock, name="test_attr", base=BASE_VAL,
                              min=MIN_VAL, max=MAX_VAL)
        self.attr.get_modified_val = Mock(return_value=MOD_VAL)

    def tearDown(self):
        self.attr = None

    def test_initial_state(self):
        self.assertEqual(self.attr.name, "test_attr")
        self.assertEqual(self.attr.base, 20)
        self.assertEqual(self.attr.min, 0)
        self.assertEqual(self.attr.max, 100)
        self.assertEqual(self.cur_val, 10)

    def test_modfiy_base(self):
        self.attr.base += 1
        self.assertEqual(self.attr.base, BASE_VAL + 1)

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
