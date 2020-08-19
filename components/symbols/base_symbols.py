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
                         "OPERATOR_ABS": 40,
                         "OPERATOR_PLUS": 30,
                         "OPERATOR_MINUS": 30,
                         "OPERATOR_LSL": 20,
                         "OPERATOR_LSR": 20,
                         "OPERATOR_XOR": 20,
                         "OPERATOR_SHL": 20,
                         "OPERATOR_SHR": 20,
                         "OPERATOR_NOT": 10,
                         "OPERATOR_AND": 10,
                         "OPERATOR_OR": 10,
                         "OPERATOR_IN": 5,
                         "OPERATOR_EQUAL_TO": 5,
                         "OPERATOR_NOT_EQUAL_TO": 5,
                         "OPERATOR_LESS_THEN": 5,
                         "OPERATOR_GREATER_THEN": 5,
                         "OPERATOR_LESS_OR_EQUAL_TO": 5,
                         "OPERATOR_GREATER_OR_EQUAL_TO": 5,
                         "OPERATOR_ASSIGNMENT": 1,
                         "LEFT_PARENTHESES": 0
                         }


    def __init__(self, a_name, a_scope=None, a_level=None, a_type=None, a_value=None):
        self._name = a_name
        self._scope = a_scope
        self._level = a_level
        self._type = self._map_to_base_type(a_type)
        self._value = a_value
        self._reference_stack = []


    def __str__(self):
        return "{0}('{1}'|{2}|{3}|{4}|{5}|{6})".format(self.category,
                                                       self.name,
                                                       self.type,
                                                       self.value,
                                                       self.scope,
                                                       self.level,
                                                       self.references)

    def __repr__(self):
        return "{0}('{1}'|{2}|{3}|{4}|{5}|{6})".format(self.category,
                                                       self.name,
                                                       self.type,
                                                       self.value,
                                                       self.scope,
                                                       self.level,
                                                       self.references)


    @classmethod
    def from_token(cls, parser_token, context_label, context_level):
        if isinstance(parser_token, Token):
            return cls(parser_token.value, context_label, context_level, parser_token.type, parser_token.value)
        else:
            raise ValueError("An instance of Token is required as parameter")

    @staticmethod
    def _map_to_base_type(a_type_name):
        """
        this maps the constant token names received from the parser to pascal language types
        it is needed for the type checking process
        applicable to all Symbols but only specialised for Constants
        """
        return a_type_name

    @property
    def precedence(self):
        return BaseSymbol._precedence_rules[self.type] if self.type in BaseSymbol._precedence_rules else 0

    @property
    def name(self):
        return self._name

    @property
    def scope(self):
        return self._scope

    @property
    def level(self):
        return self._level

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

    @scope.setter
    def scope(self, new_scope):
        self._scope = new_scope

    @level.setter
    def level(self, new_level):
        self._level = new_level

    @type.setter
    def type(self, new_type):
        self._type = self._map_to_base_type(new_type)

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def push_reference(self, reference):
        self._reference_stack.append(reference)

    def pop_reference(self):
        return self._reference_stack.pop()

    def is_equal(self, a_base_symbol, equal_class=True, equal_type=True, equal_level=True, equal_name=True):
        if isinstance(a_base_symbol, BaseSymbol):
            result = True
            if equal_class:
                result = result and (type(self) == type(a_base_symbol))
            if equal_type:
                result = result and (self._type == a_base_symbol._type)
            if equal_level:
                result = result and (self.scope == a_base_symbol.scope and self.level == a_base_symbol.level)
            if equal_name:
                result = result and (self.name == a_base_symbol.name)
            return result
        else:
            raise ValueError("instance of BaseSymbol or its sub-classes expected")

    @property
    def is_operator(self):
        return "OPERATOR_" in self.type if self.type else False

    @property
    def is_pointer(self):
        return False


class BaseIdentifier(BaseSymbol):

    def do_nothing(self):
        pass


class BaseType(BaseSymbol):

    def do_nothing(self):
        pass


class Keyword(BaseSymbol):

    def do_nothing(self):
        pass


class GenericExpression(BaseSymbol):

    @classmethod
    def from_list(cls, expression_list, a_scope=None, a_level=None):
        return cls('GENERIC_EXPRESSION', a_scope, a_level, 'GENERIC_EXPRESSION', expression_list)
