from collections import deque


class BaseSymbol:

    def __init__(self, a_name, a_level, attribute_a, attribute_b):
        self.__name = a_name
        self.__level = a_level
        self.__attribute_a = attribute_a
        self.__attribute_b = attribute_b
        self.__reference_stack = deque()

    def __str__(self):
        return("[{0}|{1}|{2}|{3}|{4}]".format(self.name,
                                              self.level,
                                              self.category,
                                              self.first_attribute,
                                              self.second_attribute))

    @property
    def name(self):
        return self.__name

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
    def has_references(self):
        if self.__reference_stack:
            return True
        else:
            return False

    @name.setter
    def name(self, new_name):
        self.__name = new_name

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

    def is_similar_to(self, a_base_symbol):
        if isinstance(a_base_symbol, BaseSymbol):
            return self.level == a_base_symbol.level and self.name == a_base_symbol.name
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
        self.__symbol_table.update({0: {}})

    def exists(self, a_symbol):
        if a_symbol.level in self.__symbol_table:
            if a_symbol.name in self.__symbol_table[a_symbol.level]:
                return a_symbol.is_similar_to(self.__symbol_table[a_symbol.level][a_symbol.name])
        else:
            return False

    def append(self, a_symbol):
        if a_symbol.level not in self.__symbol_table:
            self.__symbol_table[a_symbol.level] = {}
        #
        if a_symbol.name in self.__symbol_table[a_symbol.level]:
            raise KeyError
        #
        self.__symbol_table[a_symbol.level][a_symbol.name] = a_symbol

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

    def remove_all_from_scope(self, a_scope):
        if a_scope not in self.__symbol_table:
            raise KeyError
        #
        return self.__symbol_table.pop(a_scope)
