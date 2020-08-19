"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest.case import TestCase

from components.symbols.constant_symbols import Constant, BooleanConstant, NilConstant


class TestConstant(TestCase):
    def test_type_setter_generic_type(self):
        symbol = Constant('test_symbol')
        symbol.type = 'new_value'
        self.assertEqual('new_value', symbol.type)

    def test_type_setter_using_map_to_base_type(self):
        symbol = Constant('test_symbol')
        symbol.type = 'CONSTANT_NIL'
        self.assertEqual('RESERVED_TYPE_POINTER', symbol.type)

    def test_type_in_new_using_map_to_base_type_NIL(self):
        symbol = Constant('test_symbol', a_type='CONSTANT_NIL')
        self.assertEqual('RESERVED_TYPE_POINTER', symbol.type)

    def test_type_in_new_using_map_to_base_type_STRING(self):
        symbol = Constant('test_symbol', a_type='STRING_VALUE')
        self.assertEqual('RESERVED_TYPE_STRING', symbol.type)

    def test_type_in_new_using_map_to_base_type_CHAR(self):
        symbol = Constant('test_symbol', a_type='CHAR')
        self.assertEqual('RESERVED_TYPE_CHAR', symbol.type)
        symbol = Constant('test_symbol', a_type='CHARACTER')
        self.assertEqual('RESERVED_TYPE_CHAR', symbol.type)

    def test_type_in_new_using_map_to_base_type_REAL(self):
        symbol = Constant('test_symbol', a_type='REAL')
        self.assertEqual('RESERVED_TYPE_REAL', symbol.type)
        symbol = Constant('test_symbol', a_type='UNSIGNED_REAL')
        self.assertEqual('RESERVED_TYPE_REAL', symbol.type)
        symbol = Constant('test_symbol', a_type='SIGNED_REAL')
        self.assertEqual('RESERVED_TYPE_REAL', symbol.type)

    def test_type_in_new_using_map_to_base_type_INTEGER(self):
        symbol = Constant('test_symbol', a_type='INTEGER')
        self.assertEqual('RESERVED_TYPE_INTEGER', symbol.type)
        symbol = Constant('test_symbol', a_type='UNSIGNED_DECIMAL')
        self.assertEqual('RESERVED_TYPE_INTEGER', symbol.type)
        symbol = Constant('test_symbol', a_type='SIGNED_DECIMAL')
        self.assertEqual('RESERVED_TYPE_INTEGER', symbol.type)
        symbol = Constant('test_symbol', a_type='NUMBER_BINARY')
        self.assertEqual('RESERVED_TYPE_INTEGER', symbol.type)
        symbol = Constant('test_symbol', a_type='NUMBER_OCTAL')
        self.assertEqual('RESERVED_TYPE_INTEGER', symbol.type)
        symbol = Constant('test_symbol', a_type='NUMBER_HEXADECIMAL')
        self.assertEqual('RESERVED_TYPE_INTEGER', symbol.type)

    def test_type_in_new_using_map_to_base_type_BOOLEAN(self):
        symbol = Constant('test_symbol', a_type='BOOLEAN')
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)
        symbol = Constant('test_symbol', a_type='CONSTANT_TRUE')
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)
        symbol = Constant('test_symbol', a_type='CONSTANT_FALSE')
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)


class TestBooleanConstant(TestCase):

    def test_true(self):
        symbol = BooleanConstant.true(0, 0)
        self.assertEqual('CONSTANT_TRUE', symbol.name)
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)
        self.assertTrue(symbol.value)

    def test_false(self):
        symbol = BooleanConstant.false(0, 0)
        self.assertEqual('CONSTANT_FALSE', symbol.name)
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)
        self.assertFalse(symbol.value)

    def test_from_value_true(self):
        symbol = BooleanConstant.from_value(True, 0, 0)
        self.assertEqual('CONSTANT_TRUE', symbol.name)
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)
        self.assertTrue(symbol.value)

    def test_from_value_false(self):
        symbol = BooleanConstant.from_value(False, 0, 0)
        self.assertEqual('CONSTANT_FALSE', symbol.name)
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)
        self.assertFalse(symbol.value)

    def test_from_value_any(self):
        symbol = BooleanConstant.from_value('any_value', 0, 0)
        self.assertEqual('CONSTANT_FALSE', symbol.name)
        self.assertEqual('RESERVED_TYPE_BOOLEAN', symbol.type)
        self.assertFalse(symbol.value)


class TestNilConstant(TestCase):

    def test_nil(self):
        symbol = NilConstant.nil(0, 0)
        self.assertEqual('NIL', symbol.name)
        self.assertEqual('RESERVED_TYPE_POINTER', symbol.type)
        self.assertEqual('RESERVED_TYPE_POINTER', symbol.value)