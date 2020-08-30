"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase

from components.symbols.base_symbols import BaseSymbol
from components.symbol_table import SymbolTable

import logging

logger = logging.getLogger(__name__)


class TestSymbolTable(TestCase):

    def test_contains_name(self):
        symbol_1 = BaseSymbol('new_symbol_1', 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 'any_type', 'any_value')
        table = SymbolTable()
        table.increase_level("level_1")
        table.append(symbol_1)
        table.increase_level("level_2")
        table.append(symbol_2)
        self.assertFalse(table.contains(symbol_1.name, equal_level_only=True))
        self.assertTrue(table.contains(symbol_2.name, equal_level_only=True))
        self.assertTrue(table.contains(symbol_1.name, equal_level_only=False))


    def test_retrieve_by_name(self):
        symbol_1 = BaseSymbol('new_symbol_1', 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 'any_type', 'any_value')
        table = SymbolTable()
        table.increase_level("level_1")
        table.append(symbol_1)
        table.increase_level("level_2")
        table.append(symbol_2)
        self.assertIsNone(table.retrieve(symbol_1.name, equal_level_only=True))
        self.assertIsNotNone(table.retrieve(symbol_2.name, equal_level_only=True))
        self.assertIsNotNone(table.retrieve(symbol_1.name, equal_level_only=False))


    def test_append_already_existing(self):
        symbol_1 = BaseSymbol('new_symbol', 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol', 'any_type', 'any_value')
        table = SymbolTable()
        table.increase_level("level_1")
        table.append(symbol_1)
        self.assertRaises(KeyError, table.append, symbol_2)


    def test_remove_level_not_present(self):
        symbol_1 = BaseSymbol('new_symbol', 'any_type', 'any_value')
        table = SymbolTable()
        self.assertRaises(KeyError, table.remove, symbol_1.name)


    def test_remove_name_not_present(self):
        symbol_1 = BaseSymbol('new_symbol_1', 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 'any_type', 'any_value')
        table = SymbolTable()
        table.increase_level("level_1")
        table.append(symbol_1)
        self.assertRaises(KeyError, table.remove, symbol_2.name)


    def test_remove(self):
        symbol_1 = BaseSymbol('new_symbol_1', 'any_type', 'any_value')
        table = SymbolTable()
        table.increase_level("level_1")
        table.append(symbol_1)
        self.assertEqual(symbol_1, table.remove(symbol_1.name))


    def test_remove_same_symbol_twice_is_equivalent_as_remove_not_present_symbol(self):
        symbol_1 = BaseSymbol('new_symbol_1', 'any_type', 'any_value')
        table = SymbolTable()
        table.increase_level("level_1")
        table.append(symbol_1)
        self.assertEqual(symbol_1, table.remove(symbol_1.name))
        self.assertRaises(KeyError, table.remove, symbol_1.name)


    def test_get_level_not_present(self):
        symbol_1 = BaseSymbol('new_symbol', 'any_type', 'any_value')
        table = SymbolTable()
        self.assertRaises(KeyError, table.get, symbol_1.name)

    def test_get_name_not_present(self):
        symbol_1 = BaseSymbol('new_symbol_1', 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 'any_type', 'any_value')
        table = SymbolTable()
        table.increase_level("level_1")
        table.append(symbol_1)
        self.assertRaises(KeyError, table.get, symbol_2.name)

    def test_get(self):
        symbol_1 = BaseSymbol('new_symbol_1', 'any_type', 'any_value')
        table = SymbolTable()
        table.increase_level("level_1")
        table.append(symbol_1)
        result = table.get(symbol_1.name)
        self.assertEqual(symbol_1, result)

    def test_purge_all_from_scope(self):
        symbol_1 = BaseSymbol('new_symbol_1', 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 'any_type', 'any_value')
        table = SymbolTable()
        table.increase_level("level_1")
        table.append(symbol_1)
        table.append(symbol_2)
        table.purge_all_from_current_scope()
        self.assertRaises(KeyError, table.get, symbol_2.name)

    def test_str_repr_return_the_same(self):
        table = SymbolTable()
        self.assertEqual(str(table), table.__repr__())

    def test_current_scope(self):
        table = SymbolTable()
        a_tuple = table.increase_level("test")
        self.assertEqual(a_tuple[0], table.current_scope)

    def test_current_scope_on_empty_symbol_table_raises_key_error(self):
        table = SymbolTable()
        with self.assertRaises(KeyError) as cm:
            table.current_scope()
            self.assertIsInstance(cm.exception, KeyError)

    def test_current_level(self):
        table = SymbolTable()
        a_tuple = table.increase_level("test")
        self.assertEqual(a_tuple[1], table.current_level)
        self.assertEqual(a_tuple[0], "test")

    def test_current_level_on_empty_symbol_table_raises_key_error(self):
        table = SymbolTable()
        with self.assertRaises(KeyError) as cm:
            table.current_level()
            self.assertIsInstance(cm.exception, KeyError)

    def test_increase_level(self):
        table = SymbolTable()
        x = table.increase_level("level_0")
        y = table.increase_level("level_1")
        self.assertEqual(y[1], x[1] + 1)
        self.assertEqual(y[1], table.current_level)
        self.assertEqual(y[0], "level_1")

    def test_decrease_level(self):
        table = SymbolTable()
        a_tuple = table.increase_level("level_0")
        table.increase_level("level_1")
        table.decrease_level()
        level = table.current_level
        scope = table.current_scope
        self.assertEqual(a_tuple[0], scope)
        self.assertEqual(a_tuple[1], level)

    def test_decrease_level_on_empty_symbol_table_raises_value_error(self):
        table = SymbolTable()
        with self.assertRaises(ValueError) as cm:
            table.decrease_level()
            self.assertIsInstance(cm.exception, ValueError)

