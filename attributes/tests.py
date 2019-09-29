from evennia.utils.test_resources import EvenniaTest
from attributes.attribute import AttributeBaseValue, AttributeDerivedValue
from typeclasses.characters import Character


class AttributeTestCase(EvenniaTest):

    def setUp(self):
        super().setUp()
        self.char, errors = Character.create('character_one', self.account)

    def test_derived_attribute_cyclic_dependency(self):
        formula = formula = {'Strength': '(5 * Agility) + 10', 'Agility': 'Strength + 5'}

        strength, errors = AttributeDerivedValue.create('attribute_Strength',
                                                        obj=self.char,
                                                        attributes=[
                                                            ('name', 'Strength'),
                                                            ('min', 0),
                                                            ('max', 100),
                                                            ('formulas', formula)])
        agility, errors = AttributeDerivedValue.create('attribute_Agility',
                                                       obj=self.char,
                                                       attributes=[
                                                           ('name', 'Agility'),
                                                           ('min', 0),
                                                           ('max', 100),
                                                           ('formulas', formula)])
        with self.assertRaises(SyntaxError) as context:
            strength.value  # Strength depends on Agility, but Agility has a dependency on Strength

        self.assertTrue('Agility was mis-configured' in str(context.exception))

    def test_derived_attribute_success(self):
        formula = formula = {'Strength': '(5 * Agility) + 10'}

        strength, errors = AttributeDerivedValue.create('attribute_Strength',
                                                        obj=self.char,
                                                        attributes=[
                                                            ('name', 'Strength'),
                                                            ('min', 0),
                                                            ('max', 100),
                                                            ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=self.char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', 10),
                                                        ('formulas', formula)])

        self.assertEqual(strength.value, 60)  # (5 * 10) + 10 = 60

    def test_derived_attribute_two_layers_success(self):
        formula = {'Strength': '(5 * Agility) + 10 + Dexterity', 'Dexterity': '2 * Agility'}

        strength, errors = AttributeDerivedValue.create('attribute_Strength',
                                                        obj=self.char,
                                                        attributes=[
                                                            ('name', 'Strength'),
                                                            ('min', 0),
                                                            ('max', 100),
                                                            ('formulas', formula)])
        dexterity, errors = AttributeDerivedValue.create('attribute_Dexterity',
                                                         obj=self.char,
                                                         attributes=[
                                                             ('name', 'Dexterity'),
                                                             ('min', 0),
                                                             ('max', 100),
                                                             ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=self.char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', 10),
                                                        ('formulas', formula)])

        self.assertEqual(strength.value, 80)  # (5 * 10) + 10 + (2 * 10) = 80

    def test_derived_attribute_over_max_should_return_max(self):
        formula = formula = {'Strength': '(5 * Agility) + 10'}

        strength, errors = AttributeDerivedValue.create('attribute_Strength',
                                                        obj=self.char,
                                                        attributes=[
                                                            ('name', 'Strength'),
                                                            ('min', 0),
                                                            ('max', 100),
                                                            ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=self.char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', 20),
                                                        ('formulas', formula)])

        self.assertEqual(strength.value, 100)  # (5 * 20) + 10 = 110, but max is 100

    def test_derived_attribute_under_min_should_return_min(self):
        formula = formula = {'Strength': '(5 * Agility) + 10'}

        strength, errors = AttributeDerivedValue.create('attribute_Strength',
                                                        obj=self.char,
                                                        attributes=[
                                                            ('name', 'Strength'),
                                                            ('min', 50),
                                                            ('max', 100),
                                                            ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=self.char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', 1),
                                                        ('formulas', formula)])

        self.assertEqual(strength.value, 50)  # (5 * 1) + 10 = 15, but min is 50

    def test_base_attribute_success(self):
        formula = formula = {'Strength': '(5 * Agility) + 10'}

        should_not_matter, errors = AttributeDerivedValue.create('attribute_Strength',
                                                                 obj=self.char,
                                                                 attributes=[
                                                                        ('name', 'Strength'),
                                                                        ('min', 50),
                                                                        ('max', 100),
                                                                        ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=self.char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', 1),
                                                        ('formulas', formula)])

        self.assertEqual(agility.value, 1)

    def test_base_attribute_over_max_return_max(self):
        formula = formula = {'Strength': '(5 * Agility) + 10'}

        should_not_matter, errors = AttributeDerivedValue.create('attribute_Strength',
                                                                 obj=self.char,
                                                                 attributes=[
                                                                     ('name', 'Strength'),
                                                                     ('min', 50),
                                                                     ('max', 100),
                                                                     ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=self.char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', 101),
                                                        ('formulas', formula)])

        self.assertEqual(agility.value, 100)

    def test_base_attribute_under_min_return_min(self):
        formula = formula = {'Strength': '(5 * Agility) + 10'}

        should_not_matter, errors = AttributeDerivedValue.create('attribute_Strength',
                                                                 obj=self.char,
                                                                 attributes=[
                                                                     ('name', 'Strength'),
                                                                     ('min', 50),
                                                                     ('max', 100),
                                                                     ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=self.char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', -1),
                                                        ('formulas', formula)])

        self.assertEqual(agility.value, 0)
