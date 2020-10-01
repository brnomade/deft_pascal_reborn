"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from lark import Token
from collections import deque
import logging

_MODULE_LOGGER_ = logging.getLogger("deft_pascal_reborn")


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
        # self._reference_stack = []


    def __str__(self):
        return "{0}('{1}'|{2}|{3})".format(self.category, self.name, self.type, self.value)

    def __repr__(self):
        return "{0}('{1}'|{2}|{3})".format(self.category, self.name, self.type, self.value)

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

    #@property
    #def references(self):
    #    return self._reference_stack

    #@property
    #def has_references(self):
    #    if self._reference_stack:
    #        return True
    #    else:
    #        return False

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @type.setter
    def type(self, new_type):
        self._type = new_type

    @value.setter
    def value(self, new_value):
        self._value = new_value

    #def push_reference(self, reference):
    #    self._reference_stack.append(reference)

    #def pop_reference(self):
    #    return self._reference_stack.pop()


class BaseIdentifier(BaseSymbol):

    def do_nothing(self):
        pass


class BaseOperator(BaseSymbol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._compatible = None
        self._as_c = None

    def __str__(self):
        return "{0}({1})".format(self.category, self.type)

    def __repr__(self):
        return "{0}({1})".format(self.category, self.type)

    @property
    def to_c(self):
        return self._as_c if self._as_c else self.value


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


class BaseKeyword(BaseSymbol):

    def do_nothing(self):
        pass


class BaseExpression(BaseSymbol):

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

    def _infix_to_postfix(self):
        stack = deque()
        infix_tokens = self.value.copy()
        postfix_tokens = []
        lp = BaseOperator("LEFT_PARENTHESES", 'LEFT_PARENTHESES', "(")
        rp = BaseOperator("RIGHT_PARENTHESES", 'RIGHT_PARENTHESES', ")")

        stack.appendleft(lp)
        infix_tokens.append(rp)

        while infix_tokens:
            token = infix_tokens.pop(0)
            if not token:
                pass

            elif token.value == lp.value:
                stack.appendleft(token)

            elif token.value == rp.value:

                while not stack[0].value == lp.value:       # peek at topmost item in the stack
                    postfix_tokens.append(stack.popleft())
                stack.popleft()

            elif token.category == "BinaryOperator" or token.category == "UnaryOperator":

                # while stack and self.precedence_rules[stack[0].type] >= self.precedence_rules[token.type]:
                while stack and stack[0].precedence >= token.precedence:
                    postfix_tokens.append(stack.popleft())
                stack.appendleft(token)

            else:
                postfix_tokens.append(token)
        return postfix_tokens

    def _evaluate_to_type(self):
        """
        expression - is a list of tokens.
        """
        #
        compatible = True
        stack = []
        postfix_expression = self._infix_to_postfix()
        for token in postfix_expression:

            if isinstance(token, BaseOperator):
                symbol_right = stack.pop()
                symbol_right = symbol_right if isinstance(symbol_right, BaseType) else symbol_right.type

                if token.category == "UnaryOperator":
                    # if isinstance(token, operator_symbols.UnaryOperator):
                    result = token.evaluate_to_type(symbol_right)

                elif token.category == "BinaryOperator":
                    # elif isinstance(token, BinaryOperator):
                    symbol_left = stack.pop()
                    symbol_left = symbol_left if isinstance(symbol_left, BaseType) else symbol_left.type
                    result = token.evaluate_to_type(symbol_right=symbol_right, symbol_left=symbol_left)

                if result:
                    stack.append(result)

                else:
                    return None

            elif token:
                stack.append(token)

        return stack[-1] if isinstance(stack[-1], BaseType) else stack[-1].type

    @classmethod
    def from_list(cls, expression_list):
        """
        :return: None if the expression_list contains incompatible types
        :return: an instance of GenericExpression if the expression_list contains compatible_types.
                The returned GenericExpression is of the type of expression_list evaluation.
        """
        expression = BaseExpression(None, None, expression_list)
        result = expression._evaluate_to_type()
        if result:
            expression.type = result
            return expression
        else:
            _MODULE_LOGGER_.error("incompatible types in expression: {0}".format(expression_list))
            return None

    @property
    def cardinality(self):
        return len(self.value) if self.value else None

    def trim_cardinality_down(self):
        self.value = self.value[:1]
        self.type = self.value[-1].type

    @property
    def type(self):
        if self._type is None:
            return None
        else:
            return self._type.type if isinstance(self._type, BaseType) else self.type

    @type.setter
    def type(self, new_type):
        self._type = new_type

    @property
    def native_type(self):
        return self._type