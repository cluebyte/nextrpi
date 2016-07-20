"""
Unit test for ModifierHandler.
"""
from django.test import TestCase
from attributes.modifier import Modifier
from attributes.modifier_handler import ModifierHandler
from mock import Mock


class ModifierHandlerTestCase(TestCase):
    BASE_VAL = 10
    FLOAT_VAL = 0.5
    ADD_MOD = {
                'desc': "add modifier",
                'val': BASE_VAL,
                'dbref': 1,
                'typeclass': 'Script',
                'operator': '+'
    }
    SUB_MOD = {
                'desc': "subtract modifier",
                'val': BASE_VAL,
                'dbref': 2,
                'typeclass': 'Object',
                'operator': '-'
    }
    MULTI_MOD = {
                'desc': "multiply modifier",
                'val': BASE_VAL,
                'dbref': 3,
                'typeclass': 'Player',
                'operator': '*'
    }
    MULTI_FLOAT_MOD = {
                        'desc': "multiply modifier",
                        'val': FLOAT_VAL,
                        'dbref': 4,
                        'typeclass': 'Script',
                        'operator': '*'
    }
    RAW_MODS = [
                ADD_MOD,
                SUB_MOD,
                MULTI_MOD,
                MULTI_FLOAT_MOD
    ]

    def setUp(self):
        self.handler = ModifierHandler(self.RAW_MODS)
        self.add_mod = Modifier.factory(**self.ADD_MOD)
        self.sub_mod = Modifier.factory(**self.SUB_MOD)
        self.multi_mod = Modifier.factory(**self.MULTI_MOD)
        self.multi_float_mod = Modifier.factory(**self.MULTI_FLOAT_MOD)

    def tearDown(self):
        self.handler = None

    def unpack_modifiers(self, handler):
        mod_list = []
        for mods in handler.modifiers.values():
            mod_list = mod_list + mods
        return mod_list

    def test_initial_state(self):
        self.assertIn(self.add_mod, self.handler._raw_modifiers)
        self.assertIn(self.sub_mod, self.handler._raw_modifiers)
        self.assertIn(self.multi_mod, self.handler._raw_modifiers)
        self.assertIn(self.multi_float_mod, self.handler._raw_modifiers)
        dict_mod_values = self.unpack_modifiers(self.handler)
        self.assertIn(self.add_mod, dict_mod_values)
        self.assertIn(self.sub_mod, dict_mod_values)
        self.assertIn(self.multi_mod, dict_mod_values)
        self.assertIn(self.multi_float_mod, dict_mod_values)

    def test_get(self):
        self.assertEqual(self.add_mod, 
                        self.handler.get(self.ADD_MOD['desc']))
        self.assertEqual(self.sub_mod, 
                        self.handler.get(self.SUB_MOD['desc']))
        self.assertEqual(self.multi_mod, 
                        self.handler.get(self.MULTI_MOD['desc']))

    def test_filter_for_dbref(self):
        self.assertEqual(self.multi_mod, 
                        self.handler.get(self.MULTI_MOD['desc'], dbref=3))

    def test_filter_for_typeclass(self):
        self.assertEqual(self.multi_mod, 
                        self.handler.get(self.MULTI_MOD['desc'], 
                                        typeclass='Player'))

    def test_filter_for_val(self):
        self.assertEqual(self.multi_mod, 
                        self.handler.get(self.MULTI_MOD['desc'], 
                                    val=10))
        self.assertEqual(self.multi_float_mod, 
                        self.handler.get(self.MULTI_FLOAT_MOD['desc'], 
                                        val=0.5))

    def test_filter_for_val_negative(self):
        self.assertNotEqual(self.multi_float_mod, 
                            self.handler.get(self.MULTI_MOD['desc'], 
                            val=10))
        self.assertNotEqual(self.multi_mod, 
                            self.handler.get(self.MULTI_MOD['desc'], 
                            val=0.5))

    def test_multiple_filters(self):
        self.assertEqual(self.multi_mod, 
                        self.handler.get(self.MULTI_MOD['desc'],
                                        dbref=3,
                                        typeclass='Player',
                                        val=10))

    def test_remove(self):
        mod = self.handler.get(self.ADD_MOD['desc'])
        self.handler.remove(mod)
        self.assertNotIn(mod, self.handler.modifiers.values())
        self.assertNotIn(mod, self.handler._raw_modifiers)

    def test_all(self):
        mod_list = [self.add_mod, self.sub_mod, self.multi_mod,
                    self.multi_float_mod]
        self.assertEqual(mod_list, self.handler.all())

    def test_get_mod_val(self):
        self.assertEqual(self.handler.get_modified_val(self.BASE_VAL),
                        self.BASE_VAL 
                        * self.BASE_VAL 
                        * self.FLOAT_VAL 
                        + self.BASE_VAL 
                        - self.BASE_VAL)
