"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.symbols.base_symbols import BaseSymbol, BaseIdentifier, BaseType, Keyword, GenericExpression
from components.symbols.constant_symbols import Constant
from lark import Token

import logging

logger = logging.getLogger(__name__)


class TestBaseSymbol(TestCase):
    def test_name_property(self):
        symbol = BaseSymbol('test_symbol')
        self.assertEqual('test_symbol', symbol.name)

    def test_name_setter(self):
        symbol = BaseSymbol('test_symbol')
        symbol.name = 'new_value'
        self.assertEqual('new_value', symbol.name)

    def test_scope_property(self):
        symbol = BaseSymbol('test_symbol', a_scope='test_value')
        self.assertEqual('test_value', symbol.scope)

    def test_scope_setter(self):
        symbol = BaseSymbol('test_symbol')
        symbol.scope = 'new_value'
        self.assertEqual('new_value', symbol.scope)

    def test_level_property(self):
        symbol = BaseSymbol('test_symbol', a_level='test_value')
        self.assertEqual('test_value', symbol.level)

    def test_level_setter(self):
        symbol = BaseSymbol('test_symbol')
        symbol.level = 'new_value'
        self.assertEqual('new_value', symbol.level)

    def test_type_property(self):
        symbol = BaseSymbol('test_symbol', a_type='test_value')
        self.assertEqual('test_value', symbol.type)

    def test_type_setter(self):
        symbol = BaseSymbol('test_symbol')
        symbol.type = 'new_value'
        self.assertEqual('new_value', symbol.type)

    def test_type_setter_using_neutral_map_to_base_type(self):
        symbol = BaseSymbol('test_symbol')
        symbol.type = 'CONSTANT_NIL'
        self.assertEqual('CONSTANT_NIL', symbol.type)
        symbol = BaseSymbol('test_symbol', a_type='CONSTANT_NIL')
        self.assertEqual('CONSTANT_NIL', symbol.type)

    def test_value_property(self):
        symbol = BaseSymbol('test_symbol', a_value='test_value')
        self.assertEqual('test_value', symbol.value)

    def test_value_setter(self):
        symbol = BaseSymbol('test_symbol')
        symbol.value = 'new_value'
        self.assertEqual('new_value', symbol.value)

    def test_category_property(self):
        symbol = BaseSymbol('test_symbol')
        self.assertEqual('BaseSymbol', symbol.category)

    def test_references_property(self):
        symbol = BaseSymbol('test_symbol')
        symbol.push_reference("test_reference")
        self.assertIsInstance(symbol.references, list)

    def test_has_reference_property_empty(self):
        symbol = BaseSymbol('test_symbol')
        self.assertFalse(symbol.has_references)

    def test_has_reference_property_has_value(self):
        symbol = BaseSymbol('test_symbol')
        symbol.push_reference("test_reference")
        self.assertTrue(symbol.has_references)

    def test_push_reference(self):
        symbol = BaseSymbol('test_symbol')
        symbol.push_reference('test_reference')
        self.assertEqual('test_reference', symbol.references[0])

    def test_pop_reference(self):
        symbol = BaseSymbol('test_symbol')
        symbol.push_reference('test_reference_1')
        symbol.push_reference('test_reference_2')
        self.assertEqual('test_reference_2', symbol.pop_reference())

    def test_is_pointer(self):
        symbol = BaseSymbol('test_symbol')
        self.assertFalse(symbol.is_pointer)

    def test_is_operator(self):
        symbol = BaseSymbol('test_symbol')
        self.assertFalse(symbol.is_operator)

    def test_from_token_with_invalid_token(self):
        self.assertRaises(ValueError, BaseSymbol.from_token, "test_token", 0, 0)

    def test_from_token_with_valid_token(self):
        token = Token('test_type', 'test_value')
        symbol = BaseSymbol.from_token(token, 0, 0)
        self.assertEqual('test_value', symbol.name)
        self.assertEqual('test_value', symbol.value)
        self.assertEqual('test_type', symbol.type)

    def test_is_equal(self):
        symbol_1 = BaseSymbol('test_name', 'test_scope', 'test_level', 'test_type', 'test_value')
        symbol_2 = BaseSymbol('test_name', 'test_scope', 'test_level', 'test_type', 'test_value')
        symbol_3 = Constant('test_name', 'test_scope', 'test_level', 'test_type', 'test_value')
        scenarios = [(True, True, True, True, True, False),
                     (True, False, False, False, True, False),
                     (False, True, True, True, True, True),
                     (False, False, True, True, True, True),
                     (False, False, False, True, True, True),
                     (False, False, False, False, True, True),
                     ]
        for s in scenarios:
            self.assertEqual(s[4], symbol_1.is_equal(symbol_2, equal_class=s[0], equal_type=s[1], equal_level=s[2], equal_name=s[3]))
            self.assertEqual(s[5], symbol_1.is_equal(symbol_3, equal_class=s[0], equal_type=s[1], equal_level=s[2], equal_name=s[3]))

    def test_is_equal_incorrect_class(self):
        symbol_1 = BaseSymbol('test_name', 'test_scope', 'test_level', 'test_type', 'test_value')
        symbol_2 = "an incorrect instance"
        self.assertRaises(ValueError,symbol_1.is_equal, symbol_2)

    def test_precedence_property(self):
        symbol = BaseSymbol('test_name', 'test_scope', 'test_level', 'test_type', 'test_value')
        self.assertEqual(0, symbol.precedence)

    def test_precedence_table(self):
        for p in BaseSymbol._precedence_rules:
            symbol = BaseSymbol('test_name', 'test_scope', 'test_level', p, 'test_value')
            self.assertIsInstance(symbol.precedence, int)


class TestBaseIdentifier(TestCase):

    def test_is_instance(self):
        symbol = BaseIdentifier(0, 0)
        self.assertIsInstance(symbol, BaseIdentifier)


class TestBaseType(TestCase):

    def test_is_instance(self):
        symbol = BaseType(0, 0)
        self.assertIsInstance(symbol, BaseType)


class TestKeyword(TestCase):

    def test_is_instance(self):
        symbol = Keyword(0, 0)
        self.assertIsInstance(symbol, Keyword)


class TestGenericExpression(TestCase):

    def test_is_instance(self):
        symbol = GenericExpression(0, 0)
        self.assertIsInstance(symbol, GenericExpression)

    def test_from_list(self):
        symbol = GenericExpression.from_list([1,2,3], 0, 0)
        self.assertEqual([1,2,3], symbol.value)
        self.assertEqual('GENERIC_EXPRESSION', symbol.name)
        self.assertEqual('GENERIC_EXPRESSION', symbol.type)


