"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from lark import Token


class BaseSymbol:

    _precedence_rules = {"OPERATOR_ARITHMETIC_NEGATION": 70,
                         "OPERATOR_ARITHMETIC_NEUTRAL": 70,
                         "OPERATOR_STARSTAR": 60,
                         "OPERATOR_DIVIDE": 50,
                         "OPERATOR_DIV": 50,
                         "OPERATOR_MOD": 50,
                         "OPERATOR_MULTIPLY": 50,
                         "OPERATOR_ABS": 70,
                         "OPERATOR_PLUS": 30,
                         "OPERATOR_MINUS": 30,
                         "OPERATOR_LSL": 20,
                         "OPERATOR_LSR": 20,
                         "OPERATOR_XOR": 20,
                         "OPERATOR_SHL": 20,
                         "OPERATOR_SHR": 20,
                         "OPERATOR_NOT": 70,
                         "OPERATOR_AND": 10,
                         "OPERATOR_OR": 10,
                         "OPERATOR_UPARROW": 65,
                         "OPERATOR_IN": 5,
                         "OPERATOR_EQUAL_TO": 5,
                         "OPERATOR_NOT_EQUAL_TO": 5,
                         "OPERATOR_LESS_THAN": 5,
                         "OPERATOR_GREATER_THAN": 5,
                         "OPERATOR_LESS_OR_EQUAL_TO": 5,
                         "OPERATOR_GREATER_OR_EQUAL_TO": 5,
                         "OPERATOR_ASSIGNMENT": 1,
                         "LEFT_PARENTHESES": 0
                         }


    def __init__(self, a_name, a_type=None, a_value=None):
        self._name = a_name
        self._type = a_type
        self._value = a_value
        self._reference_stack = []


    def __str__(self):
        return "\n{0}('{1}'|{2}|{3})".format(self.category, self.name, self.type, self.value)

    def __repr__(self):
        return "\n{0}('{1}'|{2}|{3})".format(self.category, self.name, self.type, self.value)

    @classmethod
    def from_token(cls, parser_token):
        if isinstance(parser_token, Token):
            return cls.from_value(parser_token.value, parser_token.type)
        else:
            raise ValueError("An instance of Token is required as parameter")

    @classmethod
    def from_value(cls, a_value, a_type_name=None):
        return cls(str(a_value), a_type_name, a_value)

    @property
    def precedence(self):
        return BaseSymbol._precedence_rules[self.type] if self.type in BaseSymbol._precedence_rules else 0

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @property
    def category(self):
        return type(self).__name__

    @property
    def references(self):
        return self._reference_stack

    @property
    def has_references(self):
        if self._reference_stack:
            return True
        else:
            return False

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @type.setter
    def type(self, new_type):
        self._type = new_type

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def push_reference(self, reference):
        self._reference_stack.append(reference)

    def pop_reference(self):
        return self._reference_stack.pop()


class BaseIdentifier(BaseSymbol):

    def do_nothing(self):
        pass


class BaseType(BaseSymbol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._index = None

    def __str__(self):
        return "{0}({1})".format(self.category, self.type)

    def __repr__(self):
        return "{0}({1})".format(self.category, self.type)

    def __eq__(self, other):
        if not isinstance(other, BaseType):
            return False
        else:
            return self.name == other.name and self.type == other.type and self.value == other.value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, new_index):
        self._index = new_index

    @property
    def type_to_c(self):
        raise NotImplementedError("Must be implemented by BaseType subclasses")


class Keyword(BaseSymbol):

    def do_nothing(self):
        pass


class GenericExpression(BaseSymbol):

    def __str__(self):
        value_str = ""
        for i in self.value:
            if i:
                value_str = value_str + "{0}({1})|".format(i.category, i.name)
        value_str = value_str.rstrip("|")
        return "{0}[{1}]".format(self.category, value_str)

    def __repr__(self):
        value_str = ""
        for i in self.value:
            if i:
                value_str = value_str + "{0}({1})|".format(i.category, i.name)
        value_str = value_str.rstrip("|")
        return "{0}[{1}]".format(self.category, value_str)

    @classmethod
    def from_list(cls, expression_list):
        return cls('GENERIC_EXPRESSION', 'GENERIC_EXPRESSION', expression_list)
