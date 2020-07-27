from collections import deque


class BaseSymbol:

    @staticmethod
    def _map_to_base_type(a_type_name):
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
               #or "_PARENTHESES" in self.type
               # in ["OPERATOR_ASSIGNMENT",
               #               "OPERATOR_PLUS", "OPERATOR_MINUS", "OPERATOR_MULTIPLY", "OPERATOR_DIVIDE",
               #               "OPERATOR_STARSTAR",
               #               "OPERATOR_DIV", "OPERATOR_MOD", "OPERATOR_ABS",
               #               "OPERATOR_LSL", "OPERATOR_LSR", "OPERATOR_XOR", "OPERATOR_SHL", "OPERATOR_SHR",
               #               "OPERATOR_NOT", "OPERATOR_AND", "OPERATOR_OR",
               #               "OPERATOR_IN",
               #               "OPERATOR_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "OPERATOR_LESS_THEN",
               #               "OPERATOR_GREATER_THEN",
               #               "OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO",
               #               "OPERATOR_ARITHMETIC_NEGATION", "OPERATOR_ARITHMETIC_NEUTRAL"
               #               ]


class Constant(BaseSymbol):

    def do_nothing(self):
        pass


class Operator(BaseSymbol):

    @property
    def precedence(self):

        precedence_rules = {"OPERATOR_STARSTAR": 60,
                            "OPERATOR_DIVIDE": 50,
                            "OPERATOR_DIV": 50,
                            "OPERATOR_MOD": 50,
                            "OPERATOR_MULTIPLY": 50,
                            "OPERATOR_ABS": 40,
                            "OPERATOR_PLUS": 30,
                            "OPERATOR_MINUS": 30,
                            "OPERATOR_ARITHMETIC_NEGATION": 25,
                            "OPERATOR_ARITHMETIC_NEUTRAL": 25,
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
                            "OPERATOR_GREATER_OR_EQUAL_TO": 5
                            }
        #,
        #"OPERATOR_ASSIGNMENT": 1,
        #"LEFT_PARENTHESES": 0
        if self.type in precedence_rules:
            return precedence_rules[self.type]
        else:
            return 0

    def is_unary(self):
        return self.type in ["OPERATOR_NOT", "OPERATOR_ABS", "OPERATOR_ARITHMETIC_NEGATION",
                             "OPERATOR_ARITHMETIC_NEUTRAL"]

    def _test_unary_compatibility(self, symbol):
        if self.is_unary():
            return symbol.type == "RESERVED_TYPE_BOOLEAN"
        else:
            return False

    def _test_type_real_compatibility(self):
        return self.type in ["OPERATOR_ASSIGNMENT",
                             "OPERATOR_PLUS", "OPERATOR_MINUS", "OPERATOR_MULTIPLY", "OPERATOR_DIVIDE",
                             "OPERATOR_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "OPERATOR_LESS_THEN",
                             "OPERATOR_GREATER_THEN", "OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO"
                             ]

    def _test_type_integer_compatibility(self):
        return self.type in ["OPERATOR_ASSIGNMENT",
                             "OPERATOR_PLUS", "OPERATOR_MINUS", "OPERATOR_MULTIPLY", "OPERATOR_DIVIDE",
                             "OPERATOR_STARSTAR",
                             "OPERATOR_DIV", "OPERATOR_MOD",
                             "OPERATOR_LSL", "OPERATOR_LSR", "OPERATOR_SHL", "OPERATOR_SHR",
                             "OPERATOR_AND", "OPERATOR_OR", "OPERATOR_XOR",
                             "OPERATOR_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "OPERATOR_LESS_THEN",
                             "OPERATOR_GREATER_THEN",
                             "OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO"
                             ]

    def _test_type_set_compatibility(self):
        return self.type in ["OPERATOR_ASSIGNMENT",
                             "OPERATOR_PLUS", "OPERATOR_MINUS", "OPERATOR_MULTIPLY",
                             "OPERATOR_IN",
                             "OPERATOR_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "OPERATOR_LESS_THEN",
                             "OPERATOR_GREATER_THEN",
                             "OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO"
                             ]

    def _test_type_boolean_compatibility(self):
        return self.type in ["OPERATOR_ASSIGNMENT",
                             "OPERATOR_NOT", "OPERATOR_AND", "OPERATOR_OR",
                             "OPERATOR_IN",
                             "OPERATOR_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "OPERATOR_LESS_THEN",
                             "OPERATOR_GREATER_THEN",
                             "OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO"
                             ]

    def _test_type_string_compatibility(self):
        return self.type in ["OPERATOR_ASSIGNMENT", "OPERATOR_PLUS", "OPERATOR_IN", "OPERATOR_EQUAL_TO"]

    def _test_type_char_compatibility(self):
        return self.type in ["OPERATOR_ASSIGNMENT", "OPERATOR_PLUS", "OPERATOR_IN", "OPERATOR_EQUAL_TO"]

    def _evaluate_type_unary(self, symbol):
        if self.is_unary():
            if self.type == "OPERATOR_NOT":
                return symbol.type if symbol.type == "RESERVED_TYPE_BOOLEAN" else None
            if self.type == "OPERATOR_ARITHMETIC_NEGATION":
                return symbol
            else:
                raise KeyError("Unexpected unary operator '{0}'".format(self))
        else:
            raise SystemError("Incorrect call to unary operation.")

    def evaluate_type(self, symbol_right, symbol_left=None):
        if not symbol_left:
            return self._evaluate_type_unary(symbol_right)
        else:
            if self.type == "OPERATOR_IN":
                return symbol_left.type == "RESERVED_TYPE_CHAR" and symbol_right.type == "RESERVED_TYPE_STRING"
            elif self.type == "OPERATOR_STARSTAR":
                return symbol_left.type in ["RESERVED_TYPE_REAL", "RESERVED_TYPE_INTEGER"] and \
                       symbol_right.type == "RESERVED_TYPE_INTEGER"
            elif self.type == "OPERATOR_ASSIGNMENT":
                if symbol_right.type == "RESERVED_TYPE_POINTER" or symbol_right.type[0] == "^":
                    return symbol_left.type == "RESERVED_TYPE_POINTER" or symbol_left.type[0] == "^"
                else:
                    return symbol_left.type == symbol_right.type
            elif self.type == "OPERATOR_MULTIPLY":
                return symbol_left.type == symbol_right.type
            else:
                return False


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


