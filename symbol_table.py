from collections import deque


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
                                                       self.scope,
                                                       self.level,
                                                       self.value,
                                                       self.references)

    def __repr__(self):
        return "{0}('{1}'|{2}|{3}|{4}|{5}|{6})".format(self.category,
                                                       self.name,
                                                       self.type,
                                                       self.scope,
                                                       self.level,
                                                       self.value,
                                                       self.references)

    @staticmethod
    def _map_to_base_type(a_type_name):
        """
        this maps the constant token names received from the parser to pascal language types
        it is needed so for the type checking process
        """
        if a_type_name in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
            return "RESERVED_TYPE_BOOLEAN"
        elif a_type_name in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL", "NUMBER_HEXADECIMAL"]:
            return "RESERVED_TYPE_INTEGER"
        elif a_type_name in ["UNSIGNED_REAL", "SIGNED_REAL"]:
            return "RESERVED_TYPE_REAL"
        elif a_type_name in ["CHARACTER"]:
            return "RESERVED_TYPE_CHAR"
        elif a_type_name in ["STRING"]:
            return "RESERVED_TYPE_STRING"
        elif a_type_name in ["CONSTANT_NIL"]:
            return "RESERVED_TYPE_POINTER"
        else:
            return a_type_name

    @property
    def precedence(self):
        return BaseSymbol._precedence_rules[self.type] if self.type in BaseSymbol._precedence_rules else 0

    @property
    def category(self):
        return type(self).__name__

    @property
    def type(self):
        return self._type

    @property
    def scope(self):
        return self._scope

    @property
    def level(self):
        return self._level

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

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
        self._type = new_type

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
            raise NotImplementedError

    def is_operator(self):
        return "OPERATOR_" in self.type


class Constant(BaseSymbol):

    def do_nothing(self):
        pass


class Operator(BaseSymbol):

    # this is defined from the symbol_left perspective.
    _compatibility_matrix = {"OPERATOR_MULTIPLY": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_SET"],
                             "OPERATOR_PLUS": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_SET", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"],
                             "OPERATOR_DIVIDE": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"],
                             "OPERATOR_DIV": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"],
                             "OPERATOR_ASSIGNMENT": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL",  "RESERVED_TYPE_SET", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING", "RESERVED_TYPE_POINTER"],
                             "OPERATOR_EQUAL_TO": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL",  "RESERVED_TYPE_SET", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING", "RESERVED_TYPE_POINTER"],
                             "OPERATOR_NOT_EQUAL_TO": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL",  "RESERVED_TYPE_SET", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING", "RESERVED_TYPE_POINTER"],
                             "OPERATOR_STARSTAR": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"],
                             "OPERATOR_IN": ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_INTEGER"],
                             "OPERATOR_AND": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_BOOLEAN"],
                             "OPERATOR_OR": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_BOOLEAN"],
                             "OPERATOR_GREATER_THEN": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"],
                             "OPERATOR_GREATER_OR_EQUAL_TO": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"],
                             }

    def is_unary(self):
        return self.type in ["OPERATOR_NOT", "OPERATOR_ABS", "OPERATOR_ARITHMETIC_NEGATION",
                             "OPERATOR_ARITHMETIC_NEUTRAL"]

#    def _test_unary_compatibility(self, symbol):
#        if self.is_unary():
#            return symbol.type == "RESERVED_TYPE_BOOLEAN"
#        else:
#            return False
#
#    def _test_type_real_compatibility(self):
#        return self.type in ["",
#                             "", "OPERATOR_MINUS", "OPERATOR_MULTIPLY", "OPERATOR_DIVIDE",
#                             "OPERATOR_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "OPERATOR_LESS_THEN",
#                             "OPERATOR_GREATER_THEN", "OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO"
#                             ]
#
#    def _test_type_integer_compatibility(self):
#        return self.type in ["",
#                             "", "OPERATOR_MINUS", "OPERATOR_MULTIPLY", "OPERATOR_DIVIDE",
#                             "OPERATOR_STARSTAR",
#                             "OPERATOR_DIV", "OPERATOR_MOD",
#                             "OPERATOR_LSL", "OPERATOR_LSR", "OPERATOR_SHL", "OPERATOR_SHR",
#                             "", "OPERATOR_OR", "OPERATOR_XOR",
#                             "OPERATOR_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "OPERATOR_LESS_THEN",
#                             "OPERATOR_GREATER_THEN",
#                             "OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO"
#                             ]
#
#    def _test_type_set_compatibility(self):
#        return self.type in ["",
#                             "", "OPERATOR_MINUS", "OPERATOR_MULTIPLY",
#                             ,
#                             "OPERATOR_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "OPERATOR_LESS_THEN",
#                             "OPERATOR_GREATER_THEN",
#                             "OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO"
#                             ]
#
#    def _test_type_boolean_compatibility(self):
#        return self.type in ["",
#                             "OPERATOR_NOT", "", "OPERATOR_OR",
#                             "OPERATOR_IN",
#                             "OPERATOR_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "OPERATOR_LESS_THEN",
#                             "OPERATOR_GREATER_THEN",
#                             "OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO"
#                             ]
#
#    def _test_type_string_compatibility(self):
#        return self.type in ["", "OPERATOR_PLUS", "OPERATOR_IN", "OPERATOR_EQUAL_TO"]
#
#    def _test_type_char_compatibility(self):
#        return self.type in ["", "OPERATOR_PLUS", "OPERATOR_IN", "OPERATOR_EQUAL_TO"]

    def _evaluate_type_unary(self, symbol):
        if self.is_unary():
            if self.type == "OPERATOR_NOT" and symbol.type == "RESERVED_TYPE_BOOLEAN":
                return BooleanConstant.true()
            elif self.type in ["OPERATOR_ARITHMETIC_NEGATION", "OPERATOR_ARITHMETIC_NEUTRAL"] and symbol.type in ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"]:
                return Constant(None, None, None, symbol.type, None)

            else:
                raise KeyError("Unexpected unary operator '{0}'".format(self))
        else:
            raise SystemError("Incorrect call to unary operation.")

    @staticmethod
    def _test_compatibility_operator_greater_or_equal_to(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type == symbol_left.type:
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_greater_then(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type == symbol_left.type:
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_or(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            if symbol_right.type == "RESERVED_TYPE_BOOLEAN":
                return BooleanConstant.true()
            elif symbol_right.type == "RESERVED_TYPE_INTEGER":
                return Constant(None, None, None, symbol_right.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_and(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            if symbol_right.type == "RESERVED_TYPE_BOOLEAN":
                return BooleanConstant.true()
            elif symbol_right.type == "RESERVED_TYPE_INTEGER":
                return Constant(None, None, None, symbol_right.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_in(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == "RESERVED_TYPE_SET":
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_starstar(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type == "RESERVED_TYPE_INTEGER":
            return Constant(None, None, None, symbol_left.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_not_equal_to(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_equal_to(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_assignment(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == "RESERVED_TYPE_POINTER" or "^" in symbol_left.type:
            if symbol_right.type == "RESERVED_TYPE_POINTER" or "^" in symbol_left.type:
                return NilConstant.nil(None, None)
        elif symbol_left.type == symbol_right.type:
            return Constant(None, None, None, symbol_left.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_div(symbol_right, symbol_left):
        """
        integer division - accepts integer and real operands mixed together - result is always an integer
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type in ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"]:
            return Constant(None, None, None, "RESERVED_TYPE_INTEGER", None)
        return None

    @staticmethod
    def _test_compatibility_operator_divide(symbol_right, symbol_left):
        """
        real division - accepts integer and real operands mixed together - result is always a real
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type in ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"]:
            return Constant(None, None, None, "RESERVED_TYPE_REAL", None)
        return None

    @staticmethod
    def _test_compatibility_operator_plus(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            return Constant(None, None, None, symbol_left.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_multiply(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            return Constant(None, None, None, symbol_left.type, None)
        return None

    def evaluate_to_type(self, symbol_right, symbol_left=None):
        """
        the evaluation results in True or False values
        returns a subclass of BaseSymbol because the type_checking routine operates
        over a list of symbols
        checks involved:
        1 - [TESTED IN THIS METHOD] what types can be used with the operator
        2 - [TESTED IN THE OPERAND METHOD] if the types of the operands (symbol_right and symbol_left) match
        """
        if not symbol_left:
            return self._evaluate_type_unary(symbol_right)
        else:
            if symbol_left.type in Operator._compatibility_matrix[self.type]:
                if self.type == "OPERATOR_IN":
                    return self._test_compatibility_operator_in(symbol_right, symbol_left)
                if self.type == "OPERATOR_AND":
                    return self._test_compatibility_operator_and(symbol_right, symbol_left)
                if self.type == "OPERATOR_OR":
                    return self._test_compatibility_operator_or(symbol_right, symbol_left)
                if self.type == "OPERATOR_GREATER_THEN":
                    return self._test_compatibility_operator_greater_then(symbol_right, symbol_left)
                if self.type == "OPERATOR_GREATER_OR_EQUAL_TO":
                    return self._test_compatibility_operator_greater_then(symbol_right, symbol_left)
                elif self.type == "OPERATOR_STARSTAR":
                    return self._test_compatibility_operator_starstar(symbol_right, symbol_left)
                elif self.type == "OPERATOR_EQUAL_TO":
                    return self._test_compatibility_operator_equal_to(symbol_right, symbol_left)
                elif self.type == "OPERATOR_NOT_EQUAL_TO":
                    return self._test_compatibility_operator_equal_to(symbol_right, symbol_left)
                elif self.type == "OPERATOR_ASSIGNMENT":
                    return self._test_compatibility_operator_assignment(symbol_right, symbol_left)
                elif self.type == "OPERATOR_MULTIPLY":
                    return self._test_compatibility_operator_multiply(symbol_right, symbol_left)
                elif self.type == "OPERATOR_PLUS":
                    return self._test_compatibility_operator_plus(symbol_right, symbol_left)
                elif self.type == "OPERATOR_DIVIDE":
                    return self._test_compatibility_operator_divide(symbol_right, symbol_left)
                elif self.type == "OPERATOR_DIV":
                    return self._test_compatibility_operator_div(symbol_right, symbol_left)
                else:
                    raise NotImplementedError(self)
        return None

    def is_compatible_original(self, symbol_a, symbol_b=None):
        if self.is_unary():
            if symbol_b is not None:
                raise ValueError(symbol_b)
            else:
                return self._test_unary_compatibility(symbol_a)
        else:
            if not symbol_a.type == symbol_b.type:
                # Exceptions:
                # operator IN - example: 'C' in STRING
                if self.type == "OPERATOR_IN":
                    return symbol_a.type == "RESERVED_TYPE_CHAR" and symbol_b.type == "RESERVED_TYPE_STRING"
                elif self.type == "OPERATOR_STARSTAR":
                    return symbol_a.type == "RESERVED_TYPE_REAL" and symbol_b.type == "RESERVED_TYPE_INTEGER"
                else:
                    return False
            else:
                if symbol_a.type == "RESERVED_TYPE_REAL":
                    return self._test_type_real_compatibility()
                elif symbol_a.type == "RESERVED_TYPE_INTEGER":
                    return self._test_type_integer_compatibility()
                elif symbol_a.type == "RESERVED_TYPE_SET":
                    return self._test_type_set_compatibility()
                elif symbol_a.type == "RESERVED_TYPE_BOOLEAN":
                    return self._test_type_boolean_compatibility()
                elif symbol_a.type == "RESERVED_TYPE_STRING":
                    return self._test_type_string_compatibility()
                elif symbol_a.type == "RESERVED_TYPE_CHAR":
                    return self._test_type_char_compatibility()
                elif symbol_a.type == "RESERVED_TYPE_TEXT":
                    raise NotImplementedError(symbol_a)
                else:
                    raise KeyError(symbol_a)


class BooleanConstant(Constant):

    @classmethod
    def true(cls, a_scope=None, a_level=None):
        return cls('CONSTANT_TRUE', a_scope, a_level, 'RESERVED_TYPE_BOOLEAN', True)

    @classmethod
    def false(cls, a_scope=None, a_level=None):
        return cls('CONSTANT_FALSE', a_scope, a_level, 'RESERVED_TYPE_BOOLEAN', False)

    @classmethod
    def from_value(cls, value, a_scope=None, a_level=None):
        return cls.true(a_scope, a_level) if (not value or value.upper() == 'TRUE') else cls.false(a_scope, a_level)


class NilConstant(Constant):

    @classmethod
    def nil(cls, a_scope=None, a_level=None):
        return cls('CONSTANT_NIL', a_scope, a_level, 'RESERVED_TYPE_POINTER', None)


class Identifier(BaseSymbol):

    def do_nothing(self):
        pass


class SymbolTable:

    def __init__(self):
        self._symbol_table = {}

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__,
                                 self._symbol_table)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__,
                                 self._symbol_table)

    def has_equal(self, a_symbol, equal_class=True, equal_type=True, equal_level=True, equal_name=True):
        if a_symbol.level in self._symbol_table:
            if a_symbol.name in self._symbol_table[a_symbol.level]:
                return self._symbol_table[a_symbol.level][a_symbol.name].is_equal(a_symbol,
                                                                                   equal_class,
                                                                                   equal_type,
                                                                                   equal_level,
                                                                                   equal_name)
            else:
                return False
        else:
            return False

    def has_equal_at_lower_scope(self, a_symbol, equal_class=True, equal_type=True, equal_name=True):
        for i in range(a_symbol.level - 1, -1, -1):
            if i in self._symbol_table:
                if a_symbol.name in self._symbol_table[i]:
                    return self._symbol_table[i][a_symbol.name].is_equal(a_symbol,
                                                                         equal_class,
                                                                         equal_type,
                                                                         False,
                                                                         equal_name)
        return False

    def append(self, a_symbol):
        if a_symbol.level not in self._symbol_table:
            self._symbol_table[a_symbol.level] = {}
        #
        if a_symbol.name in self._symbol_table[a_symbol.level]:
            raise KeyError
        #
        element_to_append = {a_symbol.name: a_symbol}
        self._symbol_table[a_symbol.level].update(element_to_append)

    def remove(self, a_symbol):
        if a_symbol.level not in self._symbol_table:
            raise KeyError
        #
        if a_symbol.name not in self._symbol_table[a_symbol.level]:
            raise KeyError
        #
        return self._symbol_table[a_symbol.level].pop(a_symbol.name)

    def get(self, a_symbol):
        if a_symbol.level not in self._symbol_table:
            raise KeyError
        #
        if a_symbol.name not in self._symbol_table[a_symbol.level]:
            raise KeyError
        #
        return self._symbol_table[a_symbol.level][a_symbol.name]

    def get_from_lower_scope(self, a_symbol):
        for i in range(a_symbol.level - 1, -1, -1):
            if i in self._symbol_table:
                if a_symbol.name in self._symbol_table[i]:
                    return self._symbol_table[i][a_symbol.name]
        return None

    def purge_all_from_scope(self, a_symbol):
        if a_symbol.level in self._symbol_table:
            self._symbol_table[a_symbol.level] = {}


