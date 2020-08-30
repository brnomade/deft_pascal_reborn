"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest.case import TestCase


from components.symbols.literals_symbols import *
from components.symbols.type_symbols import *
from components.symbols.operator_symbols import UnaryOperator, BinaryOperator


class TestBinaryOperator(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.types_to_test = [BasicType.reserved_type_integer(),
                             BasicType.reserved_type_real(),
                             BasicType.reserved_type_set(),
                             BasicType.reserved_type_char(),
                             StringType.reserved_type_string(),
                             BasicType.reserved_type_boolean(),
                             BasicType.reserved_type_text(),
                             BasicType.reserved_type_array(),
                             BasicType.reserved_type_nil()
                             ]
        #

    def _perform_compatibility_test_with_types(self, operator):
        pt = PointerType.reserved_type_pointer()
        pt.type = BasicType.reserved_type_integer()
        self.types_to_test.append(pt)
        for i in self.types_to_test:
            for j in self.types_to_test:
                if operator.is_compatible(i, j):
                    self.assertIsNotNone(operator.evaluate_to_type(i, j))
                else:
                    self.assertIsNone(operator.evaluate_to_type(i, j))

    def _perform_creation_test(self, operator, a_label, a_representation):
        self.assertEqual(operator.name, a_label)
        self.assertEqual(operator.type, a_label)
        self.assertEqual(operator.value, a_representation)

    def test_binary_operator_creation_operator_multiply(self):
        operator = BinaryOperator.operator_multiply()
        self._perform_creation_test(operator, "OPERATOR_MULTIPLY", "*")

    def test_binary_operator_evaluate_to_type_with_types_operator_multiply(self):
        operator = BinaryOperator.operator_multiply()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_plus(self):
        operator = BinaryOperator.operator_plus()
        self._perform_creation_test(operator, "OPERATOR_PLUS", "+")

    def test_binary_operator_evaluate_to_type_with_types_operator_plus(self):
        operator = BinaryOperator.operator_plus()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_minus(self):
        operator = BinaryOperator.operator_minus()
        self._perform_creation_test(operator, "OPERATOR_MINUS", "-")

    def test_binary_operator_evaluate_to_type_with_types_operator_minus(self):
        operator = BinaryOperator.operator_minus()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_divide(self):
        operator = BinaryOperator.operator_divide()
        self._perform_creation_test(operator, "OPERATOR_DIVIDE", "/")

    def test_binary_operator_evaluate_to_type_with_types_operator_divide(self):
        operator = BinaryOperator.operator_divide()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_div(self):
        operator = BinaryOperator.operator_div()
        self._perform_creation_test(operator, "OPERATOR_DIV", "DIV")

    def test_binary_operator_evaluate_to_type_with_types_operator_div(self):
        operator = BinaryOperator.operator_div()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_assignment(self):
        operator = BinaryOperator.operator_assignment()
        self._perform_creation_test(operator, "OPERATOR_ASSIGNMENT", ":=")

    def test_binary_operator_evaluate_to_type_with_types_operator_assignment(self):
        operator = BinaryOperator.operator_assignment()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_equal_to(self):
        operator = BinaryOperator.operator_equal_to()
        self._perform_creation_test(operator, "OPERATOR_EQUAL_TO", "=")

    def test_binary_operator_evaluate_to_type_with_types_operator_equal_to(self):
        operator = BinaryOperator.operator_equal_to()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_not_equal_to(self):
        operator = BinaryOperator.operator_not_equal_to()
        self._perform_creation_test(operator, "OPERATOR_NOT_EQUAL_TO", "<>")

    def test_binary_operator_evaluate_to_type_with_types_operator_not_equal_to(self):
        operator = BinaryOperator.operator_not_equal_to()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_starstar(self):
        operator = BinaryOperator.operator_starstar()
        self._perform_creation_test(operator, "OPERATOR_STARSTAR", "**")

    def test_binary_operator_evaluate_to_type_with_types_operator_starstar(self):
        operator = BinaryOperator.operator_starstar()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_in(self):
        operator = BinaryOperator.operator_in()
        self._perform_creation_test(operator, "OPERATOR_IN", "IN")

    def test_binary_operator_evaluate_to_type_with_types_operator_in(self):
        operator = BinaryOperator.operator_in()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_and(self):
        operator = BinaryOperator.operator_and()
        self._perform_creation_test(operator, "OPERATOR_AND", "AND")

    def test_binary_operator_evaluate_to_type_with_types_operator_and(self):
        operator = BinaryOperator.operator_and()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_or(self):
        operator = BinaryOperator.operator_or()
        self._perform_creation_test(operator, "OPERATOR_OR", "OR")

    def test_binary_operator_evaluate_to_type_with_types_operator_or(self):
        operator = BinaryOperator.operator_or()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_xor(self):
        operator = BinaryOperator.operator_xor()
        self._perform_creation_test(operator, "OPERATOR_XOR", "XOR")

    def test_binary_operator_evaluate_to_type_with_types_operator_xor(self):
        operator = BinaryOperator.operator_xor()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_lsr(self):
        operator = BinaryOperator.operator_lsr()
        self._perform_creation_test(operator, "OPERATOR_LSR", "LSR")

    def test_binary_operator_evaluate_to_type_with_types_operator_lsr(self):
        operator = BinaryOperator.operator_lsr()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_lsl(self):
        operator = BinaryOperator.operator_lsl()
        self._perform_creation_test(operator, "OPERATOR_LSL", "LSL")

    def test_binary_operator_evaluate_to_type_with_types_operator_lsl(self):
        operator = BinaryOperator.operator_lsl()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_greater_than(self):
        operator = BinaryOperator.operator_greater_than()
        self._perform_creation_test(operator, "OPERATOR_GREATER_THAN", ">")

    def test_binary_operator_evaluate_to_type_with_types_operator_greater_than(self):
        operator = BinaryOperator.operator_greater_than()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_less_than(self):
        operator = BinaryOperator.operator_less_than()
        self._perform_creation_test(operator, "OPERATOR_LESS_THAN", "<")

    def test_binary_operator_evaluate_to_type_with_types_operator_less_than(self):
        operator = BinaryOperator.operator_less_than()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_greater_or_equal_to(self):
        operator = BinaryOperator.operator_greater_or_equal_to()
        self._perform_creation_test(operator, "OPERATOR_GREATER_OR_EQUAL_TO", ">=")

    def test_binary_operator_evaluate_to_type_with_types_operator_greater_or_equal_to(self):
        operator = BinaryOperator.operator_greater_or_equal_to()
        self._perform_compatibility_test_with_types(operator)

    def test_binary_operator_creation_operator_less_or_equal_to(self):
        operator = BinaryOperator.operator_less_or_equal_to()
        self._perform_creation_test(operator, "OPERATOR_LESS_OR_EQUAL_TO", "<=")

    def test_binary_operator_evaluate_to_type_with_types_operator_less_or_equal_to(self):
        operator = BinaryOperator.operator_less_or_equal_to()
        self._perform_compatibility_test_with_types(operator)


class TestUnaryOperator(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.types_to_test = [BasicType.reserved_type_integer(),
                             BasicType.reserved_type_real(),
                             BasicType.reserved_type_set(),
                             BasicType.reserved_type_char(),
                             StringType.reserved_type_string(),
                             BasicType.reserved_type_boolean(),
                             PointerType.reserved_type_pointer(),
                             BasicType.reserved_type_text(),
                             BasicType.reserved_type_array(),
                             BasicType.reserved_type_nil()
                             ]
        #

    def _perform_compatibility_test_with_types(self, operator):
        for i in self.types_to_test:
            if operator.is_compatible(i):
                self.assertIsNotNone(operator.evaluate_to_type(i))
            else:
                self.assertIsNone(operator.evaluate_to_type(i))


    def _perform_creation_test(self, operator, a_label, a_value):
        self.assertEqual(operator.name, a_label)
        self.assertEqual(operator.type, a_label)
        self.assertEqual(operator.value, a_value)

    def test_unary_operator_creation_operator_not(self):
        operator = UnaryOperator.operator_not()
        self._perform_creation_test(operator, "OPERATOR_NOT", "NOT")

    def test_unary_operator_creation_operator_abs(self):
        operator = UnaryOperator.operator_abs()
        self._perform_creation_test(operator, "OPERATOR_ABS", "ABS")

    def test_unary_operator_creation_operator_arithmetic_negation(self):
        operator = UnaryOperator.operator_arithmetic_negation()
        self._perform_creation_test(operator, "OPERATOR_ARITHMETIC_NEGATION", "-")

    def test_unary_operator_creation_operator_arithmetic_neutral(self):
        operator = UnaryOperator.operator_arithmetic_neutral()
        self._perform_creation_test(operator, "OPERATOR_ARITHMETIC_NEUTRAL", "+")

    def test_unary_operator_creation_operator_uparrow(self):
        operator = UnaryOperator.operator_uparrow()
        self._perform_creation_test(operator, "OPERATOR_UPARROW", "^")

    def test_unary_operator_evaluate_to_type_with_types_operator_not(self):
        operator = UnaryOperator.operator_not()
        self._perform_compatibility_test_with_types(operator)

    def test_unary_operator_evaluate_to_type_with_types_operator_abs(self):
        operator = UnaryOperator.operator_abs()
        self._perform_compatibility_test_with_types(operator)

    def test_unary_operator_evaluate_to_type_with_types_operator_arithmetic_negation(self):
        operator = UnaryOperator.operator_arithmetic_negation()
        self._perform_compatibility_test_with_types(operator)

    def test_unary_operator_evaluate_to_type_with_types_operator_arithmetic_neutral(self):
        operator = UnaryOperator.operator_arithmetic_neutral()
        self._perform_compatibility_test_with_types(operator)

