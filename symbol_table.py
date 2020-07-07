from collections import deque


class BaseSymbol:

    def __init__(self, a_name, a_scope, a_level, attribute_a, attribute_b):
        self.__name = a_name
        self.__scope = a_scope
        self.__level = a_level
        self.__attribute_a = attribute_a
        self.__attribute_b = attribute_b
        self.__reference_stack = []

    def __str__(self):
        return "{0}('{1}'|{2}|{3}|{4}|{5}|{6})".format(self.category,
                                                       self.name,
                                                       self.scope,
                                                       self.level,
                                                       self.first_attribute,
                                                       self.second_attribute,
                                                       self.references)

    def __repr__(self):
        return "{0}('{1}'|{2}|{3}|{4}|{5}|{6})".format(self.category,
                                                       self.name,
                                                       self.scope,
                                                       self.level,
                                                       self.first_attribute,
                                                       self.second_attribute,
                                                       self.references)

    @property
    def name(self):
        return self.__name

    @property
    def scope(self):
        return self.__scope

    @property
    def level(self):
        return self.__level

    @property
    def first_attribute(self):
        return self.__attribute_a

    @property
    def second_attribute(self):
        return self.__attribute_b

    @property
    def category(self):
        return type(self).__name__

    @property
    def references(self):
        return self.__reference_stack

    @property
    def has_references(self):
        if self.__reference_stack:
            return True
        else:
            return False

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @scope.setter
    def scope(self, new_scope):
        self.__scope = new_scope

    @level.setter
    def level(self, new_level):
        self.__level = new_level

    @first_attribute.setter
    def first_attribute(self, new_attribute):
        self.__attribute_a = new_attribute

    @second_attribute.setter
    def second_attribute(self, new_attribute):
        self.__attribute_b = new_attribute

    def push_reference(self, reference):
        self.__reference_stack.append(reference)

    def pop_reference(self):
        return self.__reference_stack.pop()

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
        self.__symbol_table = {}

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__,
                                 self.__symbol_table)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__,
                                 self.__symbol_table)

    def has_equal(self, a_symbol, equal_type=True, equal_level=True, equal_name=True):
        if a_symbol.level in self.__symbol_table:
            if a_symbol.name in self.__symbol_table[a_symbol.level]:
                return self.__symbol_table[a_symbol.level][a_symbol.name].is_equal(a_symbol,
                                                                                   equal_type,
                                                                                   equal_level,
                                                                                   equal_name)
            else:
                return False
        else:
            return False

    def has_equal_at_lower_scope(self, a_symbol, equal_type=True, equal_name=True):
        for i in range(a_symbol.level - 1, -1, -1):
            if i in self.__symbol_table:
                if a_symbol.name in self.__symbol_table[i]:
                    return self.__symbol_table[i][a_symbol.name].is_equal(a_symbol, equal_type, False, equal_name)
        return False

    def append(self, a_symbol):
        if a_symbol.level not in self.__symbol_table:
            self.__symbol_table[a_symbol.level] = {}
        #
        if a_symbol.name in self.__symbol_table[a_symbol.level]:
            raise KeyError
        #
        element_to_append = {a_symbol.name: a_symbol}
        self.__symbol_table[a_symbol.level].update(element_to_append)

    def remove(self, a_symbol):
        if a_symbol.level not in self.__symbol_table:
            raise KeyError
        #
        if a_symbol.name not in self.__symbol_table[a_symbol.level]:
            raise KeyError
        #
        return self.__symbol_table[a_symbol.level].pop(a_symbol.name)

    def get(self, a_symbol):
        if a_symbol.level not in self.__symbol_table:
            raise KeyError
        #
        if a_symbol.name not in self.__symbol_table[a_symbol.level]:
            raise KeyError
        #
        return self.__symbol_table[a_symbol.level][a_symbol.name]

    def get_from_lower_scope(self, a_symbol):
        for i in range(a_symbol.level - 1, -1, -1):
            if i in self.__symbol_table:
                if a_symbol.name in self.__symbol_table[i]:
                    return self.__symbol_table[i][a_symbol.name]
        return None

    def purge_all_from_scope(self, a_symbol):
        if a_symbol.level in self.__symbol_table:
            self.__symbol_table[a_symbol.level] = {}


