from evennia.utils.test_resources import EvenniaTest
from attributes.attribute import AttributeBaseValue, AttributeDerivedValue
from typeclasses.characters import Character


class AttributeTestCase(EvenniaTest):
    def test_derived_attribute_success(self):
        formula = {'Strength': '(5 * Agility) + 10'}

        char, errors = Character.create('character_one', self.account)

        strength, errors = AttributeDerivedValue.create('attribute_Strength',
                                                        obj=char,
                                                        attributes=[
                                                            ('name', 'Strength'),
                                                            ('min', 0),
                                                            ('max', 100),
                                                            ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', 10),
                                                        ('formulas', formula)])

        self.assertEqual(strength.value, 60)  # (5 * 10) + 10 = 60

    def test_derived_attribute_over_max_should_return_max(self):
        formula = {'Strength': '(5 * Agility) + 10'}

        char, errors = Character.create('character_one', self.account)

        strength, errors = AttributeDerivedValue.create('attribute_Strength',
                                                        obj=char,
                                                        attributes=[
                                                            ('name', 'Strength'),
                                                            ('min', 0),
                                                            ('max', 100),
                                                            ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', 20),
                                                        ('formulas', formula)])

        self.assertEqual(strength.value, 100)  # (5 * 20) + 10 = 110, but max is 100

    def test_derived_attribute_under_min_should_return_min(self):
            formula = {'Strength': '(5 * Agility) + 10'}

            char, errors = Character.create('character_one', self.account)

            strength, errors = AttributeDerivedValue.create('attribute_Strength',
                                                            obj=char,
                                                            attributes=[
                                                                ('name', 'Strength'),
                                                                ('min', 50),
                                                                ('max', 100),
                                                                ('formulas', formula)])
            agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                        obj=char,
                                                        attributes=[
                                                            ('name', 'Agility'),
                                                            ('min', 0),
                                                            ('max', 100),
                                                            ('_value', 1),
                                                            ('formulas', formula)])

            self.assertEqual(strength.value, 50)  # (5 * 1) + 10 = 15, but min is 50

    def test_base_attribute_success(self):
            formula = {'Strength': '(5 * Agility) + 10'}

            char, errors = Character.create('character_one', self.account)

            should_not_matter, errors = AttributeDerivedValue.create('attribute_Strength',
                                                                     obj=char,
                                                                     attributes=[
                                                                            ('name', 'Strength'),
                                                                            ('min', 50),
                                                                            ('max', 100),
                                                                            ('formulas', formula)])
            agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                        obj=char,
                                                        attributes=[
                                                            ('name', 'Agility'),
                                                            ('min', 0),
                                                            ('max', 100),
                                                            ('_value', 1),
                                                            ('formulas', formula)])

            self.assertEqual(agility.value, 1)

    def test_base_attribute_over_max_return_max(self):
        formula = {'Strength': '(5 * Agility) + 10'}

        char, errors = Character.create('character_one', self.account)

        should_not_matter, errors = AttributeDerivedValue.create('attribute_Strength',
                                                                 obj=char,
                                                                 attributes=[
                                                                     ('name', 'Strength'),
                                                                     ('min', 50),
                                                                     ('max', 100),
                                                                     ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', 101),
                                                        ('formulas', formula)])

        self.assertEqual(agility.value, 100)

    def test_base_attribute_under_min_return_min(self):
        formula = {'Strength': '(5 * Agility) + 10'}

        char, errors = Character.create('character_one', self.account)

        should_not_matter, errors = AttributeDerivedValue.create('attribute_Strength',
                                                                 obj=char,
                                                                 attributes=[
                                                                     ('name', 'Strength'),
                                                                     ('min', 50),
                                                                     ('max', 100),
                                                                     ('formulas', formula)])
        agility, errors = AttributeBaseValue.create('attribute_Agility',
                                                    obj=char,
                                                    attributes=[
                                                        ('name', 'Agility'),
                                                        ('min', 0),
                                                        ('max', 100),
                                                        ('_value', -1),
                                                        ('formulas', formula)])

        self.assertEqual(agility.value, 0)
