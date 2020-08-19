"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest.case import TestCase

from components.symbols.type_symbols import PointerType, CustomType, BasicType


class TestPointerType(TestCase):

    def test_is_instance(self):
        symbol = PointerType(0, 0)
        self.assertIsInstance(symbol, PointerType)

    def test_is_pointer(self):
        symbol = PointerType(0, 0)
        self.assertTrue(symbol.is_pointer)


class TestCustomType(TestCase):

    def test_is_instance(self):
        symbol = CustomType(0, 0)
        self.assertIsInstance(symbol, CustomType)


class TestBasicType(TestCase):

    def test_is_instance(self):
        symbol = BasicType(0, 0)
        self.assertIsInstance(symbol, BasicType)

    def test_reserved_type_integer(self):
        symbol = BasicType.reserved_type_integer(0, 0)
        self.assertEqual('INTEGER', symbol.name)
        self.assertEqual('RESERVED_TYPE_INTEGER', symbol.type)
        self.assertEqual('INTEGER', symbol.value)

    def test_reserved_type_real(self):
        symbol = BasicType.reserved_type_real(0, 0)
        self.assertEqual('REAL', symbol.name)
        self.assertEqual('RESERVED_TYPE_REAL', symbol.type)
        self.assertEqual('REAL', symbol.value)

    def test_reserved_type_boolean(self):
        symbol = BasicType.reserved_type_boolean(0, 0)
        self.assertEqual('BOOLEAN', symbol.name)
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)
        self.assertEqual('BOOLEAN', symbol.value)

    def test_reserved_type_char(self):
        symbol = BasicType.reserved_type_char(0, 0)
        self.assertEqual('CHAR', symbol.name)
        self.assertEqual('RESERVED_TYPE_CHAR', symbol.type)
        self.assertEqual('CHAR', symbol.value)

    def test_reserved_type_string(self):
        symbol = BasicType.reserved_type_string(0, 0)
        self.assertEqual('STRING', symbol.name)
        self.assertEqual('RESERVED_TYPE_STRING', symbol.type)
        self.assertEqual('STRING', symbol.value)

    def test_reserved_type_text(self):
        symbol = BasicType.reserved_type_text(0, 0)
        self.assertEqual('TEXT', symbol.name)
        self.assertEqual('RESERVED_TYPE_TEXT', symbol.type)
        self.assertEqual('TEXT', symbol.value)