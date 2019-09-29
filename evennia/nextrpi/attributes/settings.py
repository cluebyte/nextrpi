# Settings that define how attributes are calculated in your game.
# Attributes are defined in the ATTRIBUTE_FORMULAS dict below as follows:
#
#   'AttributeName': 'FORMULA'
#
# If the attribute is derived from other attributes, the Formula can be written like an equation,
# such as 'Strength * 10'. If the attribute is not derived by other attributes, then the special token 'BASE' should
# be used.
#
# If you do add derived attributes to your game, be sure that you do not declare a cyclic dependency.
# e.g. if Attack Power depends on Strength, do not make Strength also depend on Attack Power for its calculation.
# In this example, Strength should be a BASE attribute. i.e. its value is a numeric value, such as 10. If you do,
#  the AttributeHandler won't be initialized correctly and it will complain.
#
# Example dict:
# ATTRIBUTE_FORMULAS = {
#     'Strength': 'BASE',
#     'Dexterity': 'BASE',
#     'Health': '(Strength * 2) + 100',
#     'Attack Power': '(Strength / 2)',
#     'Armor': '(Dexterity * 5) + 100'
# }
#
# Order of operations is supported via "PMDAS":
# (Parenthesis, Multiplication, Division, Addition, Subtraction). Exponents are not supported.

ATTRIBUTE_FORMULAS = {
    # Fill in your attributes here.
}