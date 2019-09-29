"""
Attributes contain a character's traits, which can be used to calculate character performance for whatever actions.
For example, a character's strength may determine how much damage they can dish out in combat. NextRPI supports
derived attributes, which allow creators to specify other attributes as dependencies in order to derive a value.

For example, you may specify an 'Armor' attribute that is partially derived from the Agility attribute:
{'Armor': 'Agility * 100'}.
"""
from ast import parse, Num, BinOp, Add, Sub, Mult, Div, Pow, Name
from attributes.settings import ATTRIBUTE_FORMULAS
from typeclasses.scripts import Script


class AttributeValue(Script):
    """
    Contains a numeric value for a trait that an in-game entity has. e.g. strength characterizes the physical power
    of a character.

    Member variables:
        - formulas (dict of str: str): mapping of attribute names (case-sensitive) to a mathematical expression.
        - name (str): display name of the attribute. e.g. 'Dexterity', 'Strength', 'Agility'.
        - min (int): The minimum value this attribute can be.
        - max (int): The maximum value this attribute can be.
    """

    def at_script_creation(self):
        self.key = "attribute_your-attribute-name-here"
        self.persistent = True

        self.db.formulas = ATTRIBUTE_FORMULAS
        self.db.name = "AttributeName"
        self.db.min = 0
        self.db.max = 100

    @property
    def value(self):
        raise NotImplementedError("This should be implemented")


class AttributeBaseValue(AttributeValue):
    """
    An attribute that isn't derived from any other attribute.

    Member variables:
        - value (number): The value of the attribute.
    """

    def at_script_creation(self):
        self.db._value = 0

    @property
    def value(self):
        if self.db._value > self.db.max:
            return self.db.max
        if self.db._value < self.db.min:
            return self.db.min
        return self.db._value


class AttributeDerivedValue(AttributeValue):
    """
    An attribute that is derived from other attributes. This attribute will use its formula to calculate any
    attribute dependencies in order to derive its own value.

    i.e. a Baz attribute with formula: 'Foo * Bar' will calculate Foo and Bar's values and then multiply them to return
    its own value. If Foo and Bar have base values of  10, and 20, then Baz's value is 200.

    Member variables:
        - value (number): The value of the attribute.
    """

    @property
    def value(self):
        """
        Converts the formula into a tree, where the root node is the value being derived, and then recursively traverses
        the tree until all children node values are calculated.

        Returns:
            A numeric value.
        """
        attribute_dependency_tree = _parse_tree(self.db.formulas)
        try:
            val = self._evaluate_attribute_node(char=self.obj, node=attribute_dependency_tree[self.db.name])
        except RecursionError as e:
            raise SyntaxError(
                "{0} was mis-configured and has a cyclic dependency, attribute formulas used: {1}".format(
                    self.db.name, self.db.formulas))

        if val > self.db.max:
            return self.db.max
        if val < self.db.min:
            return self.db.min
        return val

    def _evaluate_attribute_node(self, char, node):
        if isinstance(node, Num):
            return node.n
        if isinstance(node, Name):
            attr = char.get_attribute(node.id)
            return attr.value
        if isinstance(node, BinOp):
            left = self._evaluate_attribute_node(char, node.left)
            right = self._evaluate_attribute_node(char, node.right)
            if isinstance(node.op, Add):
                return left + right
            elif isinstance(node.op, Sub):
                return left - right
            elif isinstance(node.op, Mult):
                return left * right
            elif isinstance(node.op, Div):
                return left / right
            elif isinstance(node.op, Pow):
                return left ** right


def _parse_tree(formulas):
    """
    Iterates through all attribute formulas and converts the formula strings into an ast.Node. This node represents
    a dependency tree that will be traversed to determine attribute values.

    Returns:
        A dict of str : ast.Node.
    """
    nodes = {}
    for attribute in formulas.keys():
        nodes[attribute] = parse(formulas[attribute], mode='eval').body
    return nodes
