"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest.case import TestCase

from components.symbols.type_symbols import PointerType, CustomType, BasicType, StringType


class TestPointerType(TestCase):

    def test_is_instance(self):
        symbol = PointerType.reserved_type_pointer()
        self.assertIsInstance(symbol, PointerType)
        self.assertEqual("POINTER", symbol.name)
        self.assertEqual("POINTER", symbol.value)
        self.assertEqual("RESERVED_TYPE_POINTER", symbol.type)

    def test_index(self):
        symbol = PointerType.reserved_type_pointer()
        self.assertEqual(6, symbol.index)


class TestCustomType(TestCase):

    def test_is_instance(self):
        symbol = CustomType("custom")
        self.assertIsInstance(symbol, CustomType)


class TestBasicType(TestCase):

    def test_is_instance(self):
        symbol = BasicType("basic_type")
        self.assertIsInstance(symbol, BasicType)

    def test_reserved_type_integer(self):
        symbol = BasicType.reserved_type_integer()
        self.assertEqual('INTEGER', symbol.name)
        self.assertEqual('RESERVED_TYPE_INTEGER', symbol.type)
        self.assertEqual('INTEGER', symbol.value)
        self.assertEqual(0, symbol.index)

    def test_reserved_type_real(self):
        symbol = BasicType.reserved_type_real()
        self.assertEqual('REAL', symbol.name)
        self.assertEqual('RESERVED_TYPE_REAL', symbol.type)
        self.assertEqual('REAL', symbol.value)
        self.assertEqual(1, symbol.index)

    def test_reserved_type_set(self):
        symbol = BasicType.reserved_type_set()
        self.assertEqual('SET', symbol.name)
        self.assertEqual('RESERVED_TYPE_SET', symbol.type)
        self.assertEqual('SET', symbol.value)
        self.assertEqual(2, symbol.index)

    def test_reserved_type_char(self):
        symbol = BasicType.reserved_type_char()
        self.assertEqual('CHAR', symbol.name)
        self.assertEqual('RESERVED_TYPE_CHAR', symbol.type)
        self.assertEqual('CHAR', symbol.value)
        self.assertEqual(3, symbol.index)

    def test_reserved_type_boolean(self):
        symbol = BasicType.reserved_type_boolean()
        self.assertEqual('BOOLEAN', symbol.name)
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)
        self.assertEqual('BOOLEAN', symbol.value)
        self.assertEqual(5, symbol.index)

    def test_reserved_type_text(self):
        symbol = BasicType.reserved_type_text()
        self.assertEqual('TEXT', symbol.name)
        self.assertEqual('RESERVED_TYPE_TEXT', symbol.type)
        self.assertEqual('TEXT', symbol.value)
        self.assertEqual(7, symbol.index)

    def test_reserved_type_array(self):
        symbol = BasicType.reserved_type_array()
        self.assertEqual('ARRAY', symbol.name)
        self.assertEqual('RESERVED_TYPE_ARRAY', symbol.type)
        self.assertEqual('ARRAY', symbol.value)
        self.assertEqual(8, symbol.index)

    def test_reserved_type_nil(self):
        symbol = BasicType.reserved_type_null()
        self.assertEqual('NIL', symbol.name)
        self.assertEqual('CONSTANT_NIL', symbol.type)
        self.assertEqual('NIL', symbol.value)
        self.assertEqual(9, symbol.index)


class TestStringType(TestCase):

    def test_reserved_type_string(self):
        symbol = StringType.reserved_type_string()
        self.assertEqual('STRING', symbol.name)
        self.assertEqual('RESERVED_TYPE_STRING', symbol.type)
        self.assertEqual('STRING', symbol.value)
        self.assertEqual(4, symbol.index)

    def test_property_dimension(self):
        symbol = StringType.reserved_type_string()
        self.assertEqual(80, symbol.dimension)

    def test_setter_dimension(self):
        symbol = StringType.reserved_type_string()
        symbol.dimension = 1
        self.assertEqual(1, symbol.dimension)

