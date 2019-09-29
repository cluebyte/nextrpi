from evennia.utils.test_resources import EvenniaTest
from attributes.attribute import AttributeBaseValue, AttributeDerivedValue
from typeclasses.characters import Character


class AttributeTestCase(EvenniaTest):
    def test_derived_attribute(self):
        formula = {'Strength': '(10 * Agility) + 100'}

        char = Character.create("character_one", self.account)

        strength = AttributeDerivedValue.create(key="attribute_strength", obj=char)
        agility = AttributeBaseValue.create(key="attribute_agility", obj=char)
        agility.db.value = 10

        self.assertEqual(strength.value, 200)
