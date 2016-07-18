"""
Unit test for modifiers.
"""
from django.test import TestCase
from attributes.modifier import (Modifier, MultiplyModifier, SubtractModifier,
                                AddModifier)
from mock import Mock


class ModifierTestCase(TestCase):

    ADD_OP = "+"
    SUB_OP = "-"
    MULTI_OP = "*"
    MOD_VAL = 50
    DBREF = 1
    BASE_VAL = 10
    FLOAT_VAL = 0.25
    TYPECLASS  = "Object"
    DESC = "test source"
    ADD_SERIAL = {
                "desc": DESC,
                "val": MOD_VAL,
                "dbref": DBREF,
                "typeclass": TYPECLASS,
                "operator": ADD_OP
    }
    SUB_SERIAL = {
                "desc": DESC,
                "val": MOD_VAL,
                "dbref": DBREF,
                "typeclass": TYPECLASS,
                "operator": SUB_OP
    }
    MULTI_SERIAL = {
                "desc": DESC,
                "val": MOD_VAL,
                "dbref": DBREF,
                "typeclass": TYPECLASS,
                "operator": MULTI_OP
    }

    def setUp(self):
        self.modifier = Modifier(desc=self.DESC, val=self.MOD_VAL,
                                dbref=self.DBREF, typeclass=self.TYPECLASS)
        self.multi_mod = MultiplyModifier(desc=self.DESC, val=self.MOD_VAL,
                                dbref=self.DBREF, typeclass=self.TYPECLASS)
        self.sub_mod = SubtractModifier(desc=self.DESC, val=self.MOD_VAL,
                                dbref=self.DBREF, typeclass=self.TYPECLASS)
        self.add_mod = AddModifier(desc=self.DESC, val=self.MOD_VAL,
                                dbref=self.DBREF, typeclass=self.TYPECLASS)

    def tearDown(self):
        self.modifier = None

    def test_initial_state(self):
        self.assertEqual(self.modifier.desc, self.DESC)
        self.assertEqual(self.modifier.val, self.MOD_VAL)
        self.assertEqual(self.modifier.dbref, self.DBREF)
        self.assertEqual(self.modifier.typeclass, "Object")

    def test_modify_val_add(self):
        self.assertEqual(self.add_mod.get_modified_val(self.BASE_VAL), 
                        self.MOD_VAL + self.BASE_VAL)

    def test_modify_val_multiply(self):
        self.assertEqual(self.multi_mod.get_modified_val(self.BASE_VAL), 
                        self.MOD_VAL * self.BASE_VAL)

    def test_modify_val_multiply_float(self):
        self.assertEqual(self.multi_mod.get_modified_val(self.FLOAT_VAL), 
                        12.5)

    def test_modify_val_sub(self):
        self.assertEqual(self.sub_mod.get_modified_val(self.BASE_VAL), 
                        self.BASE_VAL - self.MOD_VAL)

    def test_sub_op(self):
        self.assertEqual(self.sub_mod.operator, self.SUB_OP)

    def test_add_op(self):
        self.assertEqual(self.add_mod.operator, self.ADD_OP)

    def test_multi_op(self):
        self.assertEqual(self.multi_mod.operator, self.MULTI_OP)

    def test_factory_for_multiply(self):
        mod = Modifier.factory(**self.MULTI_SERIAL)
        self.assertIsInstance(mod, MultiplyModifier)

    def test_factory_for_add(self):
        mod = Modifier.factory(**self.ADD_SERIAL)
        self.assertIsInstance(mod, AddModifier)

    def test_factory_for_sub(self):
        mod = Modifier.factory(**self.SUB_SERIAL)
        self.assertIsInstance(mod, SubtractModifier)

    def test_serialize_add(self):
        self.assertEqual(self.add_mod.serialize(), self.ADD_SERIAL)

    def test_serialize_sub(self):
        self.assertEqual(self.sub_mod.serialize(), self.SUB_SERIAL)

    def test_serialize_multi(self):
        self.assertEqual(self.multi_mod.serialize(), self.MULTI_SERIAL)
