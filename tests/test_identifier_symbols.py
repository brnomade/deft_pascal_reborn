"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest.case import TestCase

from components.symbols.identifier_symbols import Identifier, PointerIdentifier, ProcedureIdentifier


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