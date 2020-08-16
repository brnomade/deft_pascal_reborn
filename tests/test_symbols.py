"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
VERSION.......: 0.1
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.symbols import BaseSymbol, Constant, BooleanConstant, NilConstant, \
                               BaseIdentifier, Identifier,  PointerIdentifier, ProcedureIdentifier, \
                               BaseType, PointerType, CustomType, BasicType, \
                               Keyword, GenericExpression, Operator
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
        symbol = Constant('test_symbol', a_type='STRING')
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


class TestBaseIdentifier(TestCase):

    def test_is_instance(self):
        symbol = BaseIdentifier(0, 0)
        self.assertIsInstance(symbol, BaseIdentifier)


class TestIdentifier(TestCase):

    def test_is_instance(self):
        symbol = Identifier(0, 0)
        self.assertIsInstance(symbol, Identifier)


class TestPointerIdentifier(TestCase):

    def test_is_instance(self):
        symbol = PointerIdentifier(0, 0)
        self.assertIsInstance(symbol, PointerIdentifier)

    def test_is_pointer(self):
        symbol = PointerIdentifier(0, 0)
        self.assertTrue(symbol.is_pointer)


class TestProcedureIdentifier(TestCase):

    def test_parameter_counter_property(self):
        symbol = ProcedureIdentifier('test_symbol')
        self.assertEqual(0, symbol.parameter_counter)

    def test_parameter_counter_setter_valid_value(self):
        symbol = ProcedureIdentifier('test_symbol')
        symbol.parameter_counter = 3
        self.assertEqual(3, symbol.parameter_counter)

    def test_parameter_counter_setter_valid_unlimited_value(self):
        symbol = ProcedureIdentifier('test_symbol')
        symbol.parameter_counter = ProcedureIdentifier.unlimited_parameters_list_size()
        self.assertEqual(-1, symbol.parameter_counter)

    def test_parameter_counter_setter_invalid_value(self):
        symbol = ProcedureIdentifier('test_symbol')
        with self.assertRaises(ValueError) as cm:
            symbol.parameter_counter = 'invalid_value'
        self.assertIsInstance(cm.exception, ValueError)

    def test_unlimited_parameters_list_size(self):
        self.assertEqual(-1, ProcedureIdentifier.unlimited_parameters_list_size())

    def test_in_built_procedure_write(self):
        symbol = ProcedureIdentifier.in_built_procedure_write()
        self.assertEqual('write', symbol.name)
        self.assertEqual('RESERVED_TYPE_POINTER', symbol.type)
        self.assertIsNone(symbol.value)

    def test_in_built_procedure_writeln(self):
        symbol = ProcedureIdentifier.in_built_procedure_writeln()
        self.assertEqual('writeln', symbol.name)
        self.assertEqual('RESERVED_TYPE_POINTER', symbol.type)
        self.assertIsNone(symbol.value)


class TestBaseType(TestCase):

    def test_is_instance(self):
        symbol = BaseType(0, 0)
        self.assertIsInstance(symbol, BaseType)


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