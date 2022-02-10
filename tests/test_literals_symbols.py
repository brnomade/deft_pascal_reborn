"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest.case import TestCase

from components.symbols.literals_symbols import Literal, BooleanLiteral, NilLiteral, StringLiteral, NumericLiteral
from components.symbols.type_symbols import BasicType
from components.symbols.base_symbols import BaseType


class TestLiteral(TestCase):

    def test_from_value_raises_exception_not_implemented_error(self):
        self.assertRaises(NotImplementedError, Literal.from_value, "INVALID")


class TestBooleanLiteral(TestCase):

    def test_true(self):
        symbol = BooleanLiteral.true()
        self.assertEqual('CONSTANT_TRUE', symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertTrue(symbol.value)

    def test_false(self):
        symbol = BooleanLiteral.false()
        self.assertEqual('CONSTANT_FALSE', symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertFalse(symbol.value)

    def test_from_value_true(self):
        symbol = BooleanLiteral.from_value(True, )
        self.assertEqual('CONSTANT_TRUE', symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertTrue(symbol.value)

    def test_from_value_false(self):
        symbol = BooleanLiteral.from_value(False, )
        self.assertEqual('CONSTANT_FALSE', symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertFalse(symbol.value)

    def test_from_value_any(self):
        symbol = BooleanLiteral.from_value('any_value', )
        self.assertEqual('CONSTANT_FALSE', symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertFalse(symbol.value)


class TestNilLiteral(TestCase):

    def test_nil(self):
        symbol = NilLiteral.nil()
        self.assertEqual('CONSTANT_NIL', symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertIsNone(symbol.value)


class TestNumericLiteral(TestCase):

    def test_from_value_integer(self):
        symbol = NumericLiteral.from_value("1", "INTEGER")
        self.assertEqual("1", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("1", symbol.value)

    def test_from_value_unsigned_decimal(self):
        symbol = NumericLiteral.from_value("1", "UNSIGNED_DECIMAL")
        self.assertEqual("1", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("1", symbol.value)

    def test_from_value_signed_decimal(self):
        symbol = NumericLiteral.from_value("1", "SIGNED_DECIMAL")
        self.assertEqual("1", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("1", symbol.value)

    def test_from_value_number_binary(self):
        symbol = NumericLiteral.from_value("1", "NUMBER_BINARY")
        self.assertEqual("1", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("1", symbol.value)

    def test_from_value_number_octal(self):
        symbol = NumericLiteral.from_value("1", "NUMBER_OCTAL")
        self.assertEqual("1", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("1", symbol.value)

    def test_from_value_number_hexadecimal(self):
        symbol = NumericLiteral.from_value("1", "NUMBER_HEXADECIMAL")
        self.assertEqual("1", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("1", symbol.value)

    def test_from_value_real(self):
        symbol = NumericLiteral.from_value("1", "REAL")
        self.assertEqual("1", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("1", symbol.value)

    def test_from_value_unsigned_real(self):
        symbol = NumericLiteral.from_value("1", "UNSIGNED_REAL")
        self.assertEqual("1", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("1", symbol.value)

    def test_from_value_number_signed_real(self):
        symbol = NumericLiteral.from_value("1", "SIGNED_REAL")
        self.assertEqual("1", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("1", symbol.value)

    def test_from_value_raises_exception_value_error(self):
        self.assertRaises(ValueError, NumericLiteral.from_value, "INVALID")


class TestStringLiteral(TestCase):

    def test_from_value_char(self):
        symbol = StringLiteral.from_value("C", "CHAR")
        self.assertEqual("C", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("C", symbol.value)


    def test_from_value_character(self):
        symbol = StringLiteral.from_value("C", "CHARACTER")
        self.assertEqual("C", symbol.name)
        self.assertIsInstance(symbol.type, BasicType)
        self.assertEqual("C", symbol.value)


    def test_from_value_string(self):
        symbol = StringLiteral.from_value("string", "STRING_VALUE")
        self.assertEqual("string", symbol.name)
        self.assertIsInstance(symbol.type, BaseType)
        self.assertEqual("string", symbol.value)


    def test_from_value_raises_exception_value_error(self):
        self.assertRaises(ValueError, StringLiteral.from_value, "INVALID")
