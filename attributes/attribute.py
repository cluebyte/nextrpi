from ast import parse, Num, BinOp, Add, Sub, Mult, Div, Pow
from attributes.settings import ATTRIBUTE_FORMULAS
from enum import Enum
from typeclasses.scripts import Script


class AttributeValue(Script):
    def at_script_creation(self):
        self.key = "attribute_your-attribute-name-here"
        self.persistent = True

        self.db.formulas = ATTRIBUTE_FORMULAS
        self.db._type = AttributeType.UNSPECIFIED
        self.db.name = "AttributeName"
        self.db.min = 0
        self.db.max = 100

    @property
    def type(self):
        return self.db._type

    @property
    def value(self):
        raise NotImplementedError("This should be implemented")


class AttributeBaseValue(AttributeValue):
    def at_script_creation(self):
        self.db._value = 0
        self.db._type = AttributeType.BASE

    @property
    def value(self):
        return self.db._value


class AttributeDerivedValue(AttributeValue):
    def at_script_creation(self):
        self.db._type = AttributeType.DERIVED

    @property
    def value(self):
        attribute_dependency_tree = _parse_tree(self.db.formulas)
        val = self._evaluate_attribute_node(char=self.obj, node=attribute_dependency_tree[self.db.name])

        if val > self.db.max:
            return self.db.max
        if val < self.db.min:
            return self.db.min

    def _evaluate_attribute_node(self, char, node):
        if isinstance(node, Num):
            return node.n
        if _derived_attribute(node):
            attr = char.get_attribute(node.id)
            return attr.value
        if isinstance(node, BinOp):
            left = self._evaluate_attribute_node(char, node.left)
            right = self._evaluate_attribute_node(char, node.right)
            if isinstance(node.op, Add):
                return left+right
            elif isinstance(node.op, Sub):
                return left-right
            elif isinstance(node.op, Mult):
                return left*right
            elif isinstance(node.op, Div):
                return left/right
            elif isinstance(node.op, Pow):
                return left**right


def _derived_attribute(op):
    return op.op is None


def _parse_tree(formulas):
    nodes = {}
    for attribute in formulas.keys():
        nodes[attribute] = parse(formulas[attribute], mode='eval')
    return nodes


class AttributeType(Enum):
    BASE = 1
    DERIVED = 2
    UNSPECIFIED = 3
