"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.symbols.base_symbols import BaseSymbol, BaseIdentifier, BaseType, BaseKeyword, BaseExpression
from components.symbols.literals_symbols import Literal
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

    def test_type_property(self):
        symbol = BaseSymbol('test_symbol', a_type='test_value')
        self.assertEqual('test_value', symbol.type)

    def test_type_setter(self):
        symbol = BaseSymbol('test_symbol')
        symbol.type = 'new_value'
        self.assertEqual('new_value', symbol.type)

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

    # def test_is_pointer(self):
    #    symbol = BaseSymbol('test_symbol')
    #    self.assertFalse(symbol.is_pointer)

    # def test_is_operator(self):
    #    symbol = BaseSymbol('test_symbol')
    #    self.assertFalse(symbol.is_operator)

    def test_from_token_with_invalid_token(self):
        self.assertRaises(ValueError, BaseSymbol.from_token, "test_token")

    def test_from_token_with_valid_token(self):
        token = Token('test_type', 'test_value')
        symbol = BaseSymbol.from_token(token)
        self.assertEqual('test_value', symbol.name)
        self.assertEqual('test_value', symbol.value)
        self.assertEqual('test_type', symbol.type)

    def test_from_value(self):
        symbol = BaseSymbol.from_value("test_value", "TEST_VALUE_TYPE")
        self.assertEqual('test_value', symbol.name)
        self.assertEqual('test_value', symbol.value)
        self.assertEqual('TEST_VALUE_TYPE', symbol.type)

    def test_precedence_property(self):
        symbol = BaseSymbol('test_name', 'test_type', 'test_value')
        self.assertEqual(0, symbol.precedence)

    def test_precedence_table(self):
        for p in BaseSymbol._precedence_rules:
            symbol = BaseSymbol('test_name', p, 'test_value')
            self.assertIsInstance(symbol.precedence, int)


class TestBaseIdentifier(TestCase):

    def test_is_instance(self):
        symbol = BaseIdentifier("base_identifier")
        self.assertIsInstance(symbol, BaseIdentifier)


class TestBaseType(TestCase):

    def test_is_instance(self):
        symbol = BaseType("base_type")
        self.assertIsInstance(symbol, BaseType)

    def test_index(self):
        symbol = BaseType("base_type")
        symbol.index = 100
        self.assertEqual(100, symbol.index)


class TestKeyword(TestCase):

    def test_is_instance(self):
        symbol = BaseKeyword("keyword")
        self.assertIsInstance(symbol, BaseKeyword)


class TestGenericExpression(TestCase):

    def test_is_instance(self):
        symbol = BaseExpression("generic")
        self.assertIsInstance(symbol, BaseExpression)

    def test_from_list(self):
        symbol = BaseExpression.from_list([1, 2, 3])
        self.assertEqual([1,2,3], symbol.value)
        self.assertEqual('GENERIC_EXPRESSION', symbol.name)
        self.assertEqual('GENERIC_EXPRESSION', symbol.type)


