"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest.case import TestCase

from components.symbols.base_symbols import BaseSymbol
from components.symbols.constant_symbols import BooleanConstant, Constant
from components.symbols.operator_symbols import Operator


class TestOperator(TestCase):

    def test_is_unary(self):
        symbol = Operator('test_operator')
        symbol.type = 'OPERATOR_NOT'
        self.assertTrue(symbol.is_unary())
        symbol.type = 'OPERATOR_ABS'
        self.assertTrue(symbol.is_unary())
        symbol.type = 'OPERATOR_ARITHMETIC_NEGATION'
        self.assertTrue(symbol.is_unary())
        symbol.type = 'OPERATOR_ARITHMETIC_NEUTRAL'
        self.assertTrue(symbol.is_unary())

    def test_evaluate_to_type_for_unary_invalid_unary_operator(self):
        symbol_1 = Operator('test_operator')
        symbol_1.type = 'anything'
        symbol_2 = BaseSymbol('test_symbol')
        self.assertRaises(TypeError, symbol_1.evaluate_to_type, symbol_2)

    def test_evaluate_to_type_for_unary_not_implemented_operation(self):
        symbol_1 = Operator('test_operator')
        symbol_1.type = 'OPERATOR_NOT'
        symbol_2 = BaseSymbol('test_symbol')
        self.assertRaises(NotImplementedError, symbol_1.evaluate_to_type, symbol_2)

    def test_evaluate_to_type_for_unary_not_with_boolean(self):
        symbol_1 = Operator('test_operator')
        symbol_1.type = 'OPERATOR_NOT'
        symbol_2 = BaseSymbol('test_symbol')
        symbol_2.type = 'RESERVED_TYPE_BOOLEAN'
        result = symbol_1.evaluate_to_type(symbol_2)
        self.assertIsInstance(result, BooleanConstant)

    def test_evaluate_to_type_for_unary_negation_with_integer(self):
        symbol_1 = Operator('test_operator')
        symbol_1.type = 'OPERATOR_ARITHMETIC_NEGATION'
        symbol_2 = BaseSymbol('test_symbol')
        symbol_2.type = 'RESERVED_TYPE_INTEGER'
        result = symbol_1.evaluate_to_type(symbol_2)
        self.assertIsInstance(result, Constant)