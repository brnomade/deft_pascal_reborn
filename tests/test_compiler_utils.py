"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from utils.compiler_utils import convert_to_postfix, ExpressionOriginal
from components.symbols.operator_symbols import BinaryOperator, UnaryOperator, NeutralOperator
from components.symbols.literals_symbols import BooleanLiteral, NumericLiteral
from components.symbols.type_symbols import BasicType


class TestCompilerInternals(TestCase):

    @staticmethod
    def _convert_to_tokens(expression):
        token_list = []
        for i in (expression.strip().split(" ")):
            if i == '+':
                t = BinaryOperator.operator_plus()
            elif i == '-':
                t = BinaryOperator.operator_minus()
            elif i == '*':
                t = BinaryOperator.operator_multiply()
            elif i == '/':
                t = BinaryOperator.operator_divide()
            elif i == '^' or i == "**":
                t = BinaryOperator.operator_starstar()
                t.value = '^'
            elif i == '(':
                t = NeutralOperator.operator_left_parentheses()
            elif i == ')':
                t = NeutralOperator.operator_right_parentheses()
            else:
                t = NumericLiteral.from_value(i, "INTEGER")
            token_list.append(t)
        return token_list


    def _perform_postfix_conversion_test(self, infix_expression):
        print("\ninfix expression: {0} \n".format(infix_expression))
        symbol_list = self._convert_to_tokens(infix_expression)
        #
        result = convert_to_postfix(symbol_list)
        print("\npostfix expression: {0} \n".format([i.value for i in result]))
        #
        self.assertEqual(ExpressionOriginal(infix_expression).Evaluate(),
                         [int(i.value) if i.value.isnumeric() else i.value for i in result]
                         )

    def test_postfix_original_expression_5(self):
        """
        2 ^ 5
        """
        self._perform_postfix_conversion_test(" 2 ^ 5 ")

    def test_postfix_original_expression_4(self):
        """
        110 + 50
        """
        self._perform_postfix_conversion_test(" 110 + 50 ")

    def test_postfix_original_expression_3(self):
        """
        ( 110 + 50 ) * ( 2 - 4 )
        """
        self._perform_postfix_conversion_test(" ( 110 + 50 ) * ( 2 - 4 ) ")

    def test_postfix_original_expression_2(self):
        """
        0 - 8 - 0 - 5 ^ 3
        """
        self._perform_postfix_conversion_test(" 0 - 8 - 0 - 5 ^ 3 ")

    def test_postfix_original_expression_1(self):
        """
        110 + 50 + ( 4 - 2 * 5 ) - 10 + 40
        """
        self._perform_postfix_conversion_test(" 110 + 50 + ( 4 - 2 * 5 ) - 10 + 40 ")

    def test_postfix_expression_6f(self):
        """
        1 ^ 2 ^ 3
        """
        self._perform_postfix_conversion_test(" 1 ^ 2 ^ 3")

    def test_postfix_expression_6e(self):
        """
        ( 1 ^ 2 ) ^ 3
        """
        self._perform_postfix_conversion_test("( 1 ^ 2 ) ^ 3")

    def test_postfix_expression_6d(self):
        """
        (1 ^ 2)
        """
        self._perform_postfix_conversion_test(" ( 1 ^ 2 ) ")

    def test_postfix_expression_6c(self):
        """
        ( 1 - 5 ) ^ 2
        """
        self._perform_postfix_conversion_test("( 1 - 5 ) ^ 2")

    def test_postfix_expression_6b(self):
        """
        ( 1 - 5 ) ^ 2 ^ 3
        """
        self._perform_postfix_conversion_test("( 1 - 5 ) ^ 2 ^ 3")

    def test_postfix_expression_6a(self):
        """
        2 / ( 1 - 5 ) ^ 2 ^ 3
        """
        self._perform_postfix_conversion_test("2 / ( 1 - 5 ) ^ 2 ^ 3")

    def test_postfix_expression_6_1(self):
        """
        3 + 4 * 2 / ( 1 - 5 )
        """
        self._perform_postfix_conversion_test(" 3 + 4 * 2 / ( 1 - 5 ) ")

    def test_postfix_expression_6(self):
        """
        3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3
        """
        self._perform_postfix_conversion_test("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3")

    def test_postfix_expression_5(self):
        """
        3 ^ 2 / ( 5 * 1 ) + 10
        """
        self._perform_postfix_conversion_test("3 ^ 2 / ( 5 * 1 ) + 10")

    def test_postfix_expression_4(self):
        """
        ( 110 + 50 ) * ( 2 - 4 )
        """
        self._perform_postfix_conversion_test("( 110 + 50 ) * ( 2 - 4 )")

    def test_postfix_expression_3(self):
        """
        110 + 50
        """
        #
        self._perform_postfix_conversion_test("110 + 50")

    def test_postfix_expression_1_e(self):
        """
        1 * ( 1  + 2 )
        """
        self._perform_postfix_conversion_test("1 * ( 1 + 2 )")

    def test_postfix_expression_1_d(self):
        """
        1 * 1  + 2
        """
        self._perform_postfix_conversion_test("1 * 1 + 2")

    def test_postfix_expression_1_c(self):
        """
        ( 1 * 1 ) + 2
        """
        self._perform_postfix_conversion_test("( 1 * 1 ) + 2")

    def test_postfix_expression_1_b(self):
        """
        ( 1 + 1 ) * 2
        """
        self._perform_postfix_conversion_test("( 1 + 1 ) * 2")

    def test_postfix_expression_1_a(self):
        """
         1 + 1 * 2
        """
        self._perform_postfix_conversion_test("1 + 1 * 2")

    def test_postfix_expression_1(self):
        """
         1 + 1
        """
        self._perform_postfix_conversion_test("1 + 1")


    # def test_type_check_scenario_assignment_unary_operation_compatible_type(self):
    #     #
    #     symbol_list = [
    #         BooleanLiteral.false(),
    #         BinaryOperator.operator_assignment(),
    #         UnaryOperator.operator_not(),
    #         BooleanLiteral.false(),
    #     ]
    #     #
    #     result = check_type_compatibility(symbol_list)
    #     self.assertTrue(result)
    # 
    # def test_type_check_scenario_assignment_unary_operation_not_compatible_type(self):
    #     #
    #     symbol_list = [
    #         NumericLiteral("1", None, None, BasicType.reserved_type_integer(), 1),
    #         BinaryOperator.operator_assignment(),
    #         UnaryOperator.operator_not(),
    #         BooleanLiteral.false(),
    #     ]
    #     #
    #     result = check_type_compatibility(symbol_list)
    #     self.assertFalse(result)
    # 
    # def test_type_check_scenario_expression_unary_operation_compatible_type(self):
    #     #
    #     symbol_list = [
    #         UnaryOperator.operator_not(),
    #         BooleanLiteral.false(),
    #     ]
    #     #
    #     result = check_type_compatibility(symbol_list)
    #     self.assertTrue(result)
    # 
    # def test_type_check_scenario_expression_unary_operation_not_compatible_type(self):
    #     #
    #     symbol_list = [
    #         UnaryOperator.operator_not(),
    #         NumericLiteral("1", None, None, BasicType.reserved_type_integer(), 1)
    #     ]
    #     #
    #     result = check_type_compatibility(symbol_list)
    #     self.assertFalse(result)
    # 
    # def test_type_check_scenario_assignment_single_level_not_compatible_types(self):
    #     #
    #     symbol_list = [
    #         NumericLiteral("1", None, None, BasicType.reserved_type_integer(), 1),
    #         BinaryOperator.operator_assignment(),
    #         BooleanLiteral.false(),
    #     ]
    #     #
    #     result = check_type_compatibility(symbol_list)
    #     self.assertFalse(result)
    # 
    # def test_type_check_scenario_assignment_single_level_compatible_types(self):
    #     #
    #     symbol_list = [
    #         BooleanLiteral.true(),
    #         BinaryOperator.operator_assignment(),
    #         BooleanLiteral.false(),
    #     ]
    #     #
    #     result = check_type_compatibility(symbol_list)
    #     self.assertTrue(result)
