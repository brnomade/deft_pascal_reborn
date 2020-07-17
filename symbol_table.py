from collections import deque


class BaseSymbol:

    def __init__(self, a_name, a_scope=None, a_level=None, a_type=None, a_value=None):
        self._name = a_name
        self._scope = a_scope
        self._level = a_level
        self._type = a_type
        self._value = a_value
        self._reference_stack = []

    def __str__(self):
        return "{0}('{1}'|{2}|{3}|{4}|{5}|{6})".format(self.category,
                                                       self.name,
                                                       self.scope,
                                                       self.level,
                                                       self.type,
                                                       self.value,
                                                       self.references)

    def __repr__(self):
        return "{0}('{1}'|{2}|{3}|{4}|{5}|{6})".format(self.category,
                                                       self.name,
                                                       self.scope,
                                                       self.level,
                                                       self.type,
                                                       self.value,
                                                       self.references)

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
        self._type = new_type

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def push_reference(self, reference):
        self._reference_stack.append(reference)

    def pop_reference(self):
        return self._reference_stack.pop()

    def is_equal(self, a_base_symbol, equal_type=True, equal_level=True, equal_name=True):
        if isinstance(a_base_symbol, BaseSymbol):
            result = True
            if equal_type:
                result = result and (type(self) == type(a_base_symbol))
            if equal_level:
                result = result and (self.scope == a_base_symbol.scope and self.level == a_base_symbol.level)
            if equal_name:
                result = result and (self.name == a_base_symbol.name)
            return result
        else:
            raise NotImplementedError


class IntegerVariable(BaseSymbol):

    def do_nothing(self):
        pass


class BooleanVariable(BaseSymbol):

    def do_nothing(self):
        pass


class EnumeratedVariable(BaseSymbol):

    def do_nothing(self):
        pass


class EnumeratedField(BaseSymbol):

    def do_nothing(self):
        pass


class Variable(BaseSymbol):

    def do_nothing(self):
        pass


class Constant(BaseSymbol):

    def do_nothing(self):
        pass


class Operator(BaseSymbol):

    def do_nothing(self):
        pass


class Procedure(BaseSymbol):

    def do_nothing(self):
        pass


class Function(BaseSymbol):

    def do_nothing(self):
        pass


class Label(BaseSymbol):

    def do_nothing(self):
        pass


class Parameter(BaseSymbol):

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

    def has_equal(self, a_symbol, equal_type=True, equal_level=True, equal_name=True):
        if a_symbol.level in self._symbol_table:
            if a_symbol.name in self._symbol_table[a_symbol.level]:
                return self._symbol_table[a_symbol.level][a_symbol.name].is_equal(a_symbol,
                                                                                   equal_type,
                                                                                   equal_level,
                                                                                   equal_name)
            else:
                return False
        else:
            return False

    def has_equal_at_lower_scope(self, a_symbol, equal_type=True, equal_name=True):
        for i in range(a_symbol.level - 1, -1, -1):
            if i in self._symbol_table:
                if a_symbol.name in self._symbol_table[i]:
                    return self._symbol_table[i][a_symbol.name].is_equal(a_symbol, equal_type, False, equal_name)
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


