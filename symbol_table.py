from symbols import BaseSymbol


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


    def contains_name(self, a_name, context_label, context_level, equal_level_only=True):
        a_symbol = BaseSymbol(a_name, context_label, context_level, None, None)
        result = self.has_equal(a_symbol, False, False, True, True)
        if equal_level_only:
            return result
        else:
            return result or self.has_equal_at_lower_scope(a_symbol, False, False, True)


    def retrieve_by_name(self, a_name, context_label, context_level, equal_level_only=True):
        a_symbol = BaseSymbol(a_name, context_label, context_level, None, None)
        if self.has_equal(a_symbol, False, False, True, True):
            return self.get(a_symbol)
        elif equal_level_only:
            return None
        else:
            return self.get_from_lower_scope(a_symbol)


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
            return None
        #
        if a_symbol.name not in self._symbol_table[a_symbol.level]:
            return None
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


