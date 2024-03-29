"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""


class SymbolTable:

    def __init__(self):
        self._symbol_table = {}
        self._stack_scope = []
        self._current_level = 0

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self._symbol_table)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self._symbol_table)


    def contains(self, name, equal_level_only=True):
        result = self.retrieve(name, equal_level_only)
        return result is not None

    def instances_of(self, a_class):
        """
        returns a list containing all the names of objects that are instances of a_class
        """
        result = []
        for level_dictionary in self._symbol_table.values():
            for symbol in level_dictionary.values():
                if isinstance(symbol, a_class):
                    result.append(symbol.name)
        return result

    def append(self, a_symbol):
        """
        The incoming symbol will be appended to the current symbol table level
        """
        if self.current_level not in self._symbol_table:
            self._symbol_table[self.current_level] = {}
        #
        if a_symbol.name in self._symbol_table[self.current_level]:
            raise KeyError("symbol '{0}' already present at level '{1}-{2}'".format(a_symbol, self.current_level, self.current_scope))
        #
        element_to_append = {a_symbol.name: a_symbol}
        self._symbol_table[self.current_level].update(element_to_append)


    def get(self, name, equal_level_only=True):
        if self.current_level not in self._symbol_table:
            raise KeyError("no symbols present at level '{0}-{1}'".format(self.current_level, self.current_scope))
        #
        if name not in self._symbol_table[self.current_level]:
            if equal_level_only:
                raise KeyError("symbol '{0}' not present at level '{0}-{1}'".format(self.current_level, self.current_scope))
            else:
                result = self._get_from_lower_scope(name)
                if not result:
                    raise KeyError("symbol '{0}' not found".format(name))
        else:
            result = self._symbol_table[self.current_level][name]
        #
        return result


    def _retrieve_from_level(self, name, level):
        if level not in self._symbol_table:
            result = None
        elif name not in self._symbol_table[level]:
            result = None
        else:
            result = self._symbol_table[level][name]
        return result


    def _recursive_retrieve(self, name, level):
        result = self._retrieve_from_level(name, level)
        if not result and level > 0:
            result = self._recursive_retrieve(name, level - 1)
        return result


    def retrieve(self, name, equal_level_only=True):
        if equal_level_only:
            return self._retrieve_from_level(name, self.current_level)
        else:
            return self._recursive_retrieve(name, self.current_level)
        #                 if self.current_level not in self._symbol_table:
        #                 result = None
        #             elif name not in self._symbol_table[self.current_level]:
        #                 result = None
        #             else:
        #                 result = self._symbol_table[self.current_level][name]
        #         else:
        #             if self.current_level not in self._symbol_table:
        #                 result = self._get_from_lower_scope(name)
        #
        #                 if name not in self._symbol_table[self.current_level]:
        #
        #         if self.current_level not in self._symbol_table:
        #             result = None
        #         elif name not in self._symbol_table[self.current_level]:
        #             if equal_level_only:
        #                 result = None
        #             else:
        #                 result = self._get_from_lower_scope(name)
        #         else:
        #             result = self._symbol_table[self.current_level][name]
        #         #
        #         return result
        #

    def _get_from_lower_scope(self, name):
        for i in range(self.current_level - 1, -1, -1):
            if i in self._symbol_table:
                if name in self._symbol_table[i]:
                    return self._symbol_table[i][name]
        return None


    def purge_all_from_current_scope(self):
        self._symbol_table[self.current_level] = {}


    def remove(self, name):
        if self.current_level not in self._symbol_table:
            raise KeyError("no symbols present  at level '{0}-{1}'".format(self.current_level, self.current_scope))
        #
        if name not in self._symbol_table[self.current_level]:
            raise KeyError("symbol '{0}' not present at level '{0}-{1}'".format(self.current_level, self.current_scope))
        #
        return self._symbol_table[self.current_level].pop(name)


    def replace(self, name, symbol):
        """
        The incoming symbol will replace an already present symbol identified by name at the current level
        """
        if not self.contains(name, equal_level_only=True):
            raise KeyError("symbol '{0}' not present at level '{1}'".format(name, self.current_level))
        else:
            self._symbol_table[self.current_level][name] = symbol


    @property
    def current_scope(self):
        if self._stack_scope:
            return self._stack_scope[-1][0]
        else:
            raise KeyError("stack scope is currently empty")

    @property
    def current_level(self):
        if self._stack_scope:
            return self._stack_scope[-1][1]
        else:
            raise KeyError("stack scope is currently empty")


    def increase_level(self, a_scope):
        self._current_level = self._current_level + 1
        self._stack_scope.append((a_scope, self._current_level))
        return self._stack_scope[-1]


    def decrease_level(self):
        if self._current_level > 0:
            self.purge_all_from_current_scope()
            self._stack_scope.pop()
            self._current_level = self._current_level - 1
            return self._stack_scope[-1]
        else:
            raise ValueError("stack scope is at lowest level")
