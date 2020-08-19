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
        symbol_1 = BaseSymbol('new_symbol_1', 0, 0, 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 1, 1, 'any_type', 'any_value')
        table = SymbolTable()
        table.append(symbol_1)
        table.append(symbol_2)
        self.assertTrue(table.contains_name(symbol_1.name, 0, 0, equal_level_only=True))
        self.assertFalse(table.contains_name(symbol_1.name, 1, 1, equal_level_only=True))
        self.assertTrue(table.contains_name(symbol_1.name, 1, 1, equal_level_only=False))


    def test_retrieve_by_name(self):
        symbol_1 = BaseSymbol('new_symbol_1', 0, 0, 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 1, 1, 'any_type', 'any_value')
        table = SymbolTable()
        table.append(symbol_1)
        table.append(symbol_2)
        self.assertEqual(symbol_1, table.retrieve_by_name(symbol_1.name, 0, 0, equal_level_only=True))
        self.assertIsNone(table.retrieve_by_name(symbol_1.name, 1, 1, equal_level_only=True))
        self.assertEqual(symbol_1, table.retrieve_by_name(symbol_1.name, 1, 1, equal_level_only=False))


    def test_append_already_existing(self):
        symbol_1 = BaseSymbol('new_symbol', 0, 0, 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol', 0, 0, 'any_type', 'any_value')
        table = SymbolTable()
        table.append(symbol_1)
        self.assertRaises(KeyError, table.append, symbol_2)


    def test_remove_level_not_present(self):
        symbol_1 = BaseSymbol('new_symbol', 0, 0, 'any_type', 'any_value')
        table = SymbolTable()
        self.assertRaises(KeyError, table.remove, symbol_1)


    def test_remove_name_not_present(self):
        symbol_1 = BaseSymbol('new_symbol_1', 0, 0, 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 0, 0, 'any_type', 'any_value')
        table = SymbolTable()
        table.append(symbol_1)
        self.assertRaises(KeyError, table.remove, symbol_2)


    def test_remove(self):
        symbol_1 = BaseSymbol('new_symbol_1', 0, 0, 'any_type', 'any_value')
        table = SymbolTable()
        table.append(symbol_1)
        self.assertEqual(symbol_1, table.remove(symbol_1))
        self.assertRaises(KeyError, table.remove, symbol_1)


    def test_get_level_not_present(self):
        symbol_1 = BaseSymbol('new_symbol', 0, 0, 'any_type', 'any_value')
        table = SymbolTable()
        self.assertRaises(KeyError, table.get, symbol_1)

    def test_get_name_not_present(self):
        symbol_1 = BaseSymbol('new_symbol_1', 0, 0, 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 0, 0, 'any_type', 'any_value')
        table = SymbolTable()
        table.append(symbol_1)
        self.assertRaises(KeyError, table.get, symbol_2)

    def test_get(self):
        symbol_1 = BaseSymbol('new_symbol_1', 0, 0, 'any_type', 'any_value')
        table = SymbolTable()
        table.append(symbol_1)
        result = table.get(symbol_1)
        self.assertEqual(symbol_1, result)

    def test_purge_all_from_scope(self):
        symbol_1 = BaseSymbol('new_symbol_1', 0, 0, 'any_type', 'any_value')
        symbol_2 = BaseSymbol('new_symbol_2', 0, 0, 'any_type', 'any_value')
        table = SymbolTable()
        table.append(symbol_1)
        table.append(symbol_2)
        table.purge_all_from_scope(symbol_1)
        self.assertRaises(KeyError, table.get, symbol_2)

    def test_has_equal_scenario_not_tested_by_other_tests(self):
        symbol_1 = BaseSymbol('new_symbol_1', 0, 0, 'any_type', 'any_value')
        table = SymbolTable()
        self.assertFalse(table.has_equal(symbol_1))

    def test_str_repr_return_the_same(self):
        table = SymbolTable()
        self.assertEqual(str(table), table.__repr__())