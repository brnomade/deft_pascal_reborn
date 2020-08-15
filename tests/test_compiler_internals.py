"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
VERSION.......: 0.1
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from utils.compiler_utils import check_type_compatibility, convert_to_postfix, convert_to_tokens, ExpressionOriginal
from components.symbols import BooleanConstant, Constant, Operator
import logging

logger = logging.getLogger(__name__)


class TestCompilerInternals(TestCase):

    def _perform_postfix_conversion_test(self, infix_expression):
        print("\ninfix expression: {0} \n".format(infix_expression))
        symbol_list = convert_to_tokens(infix_expression)
        #
        result = convert_to_postfix(symbol_list)
        print("\npostfix expression: {0} \n".format([i.value for i in result]))
        #
        self.assertEqual(ExpressionOriginal(infix_expression).Evaluate(),
                         [i.value for i in result]
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


    def x_test_type_check_scenario_assignment_unary_operation_compatible_type(self):
        #
        symbol_list = [
            BooleanConstant.false(),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            Operator("NOT", None, None, "OPERATOR_NOT", "NOT"),
            BooleanConstant.false(),
        ]
        #
        result = check_type_compatibility(symbol_list)
        self.assertTrue(result)

    def x_test_type_check_scenario_assignment_unary_operation_not_compatible_type(self):
        #
        symbol_list = [
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            Operator("NOT", None, None, "OPERATOR_NOT", "NOT"),
            BooleanConstant.false(),
        ]
        #
        result = check_type_compatibility(symbol_list)
        self.assertFalse(result)

    def x_test_type_check_scenario_expression_unary_operation_compatible_type(self):
        #
        symbol_list = [
            Operator("NOT", None, None, "OPERATOR_NOT", "NOT"),
            BooleanConstant.false(),
        ]
        #
        result = check_type_compatibility(symbol_list)
        self.assertTrue(result)

    def x_test_type_check_scenario_expression_unary_operation_not_compatible_type(self):
        #
        symbol_list = [
            Operator("NOT", None, None, "OPERATOR_NOT", "NOT"),
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
        ]
        #
        result = check_type_compatibility(symbol_list)
        self.assertFalse(result)

    def x_test_type_check_scenario_assignment_single_level_not_compatible_types(self):
       #
        symbol_list = [
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            BooleanConstant.false(),
        ]
        #
        result = check_type_compatibility(symbol_list)
        self.assertFalse(result)

    def x_test_type_check_scenario_assignment_single_level_compatible_types(self):
        #
        symbol_list = [
            BooleanConstant.true(),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            BooleanConstant.false(),
        ]
        #
        result = check_type_compatibility(symbol_list)
        self.assertTrue(result)

    def DONOTRUN_test_type_check_scenario_expression_single_level_compatible_types(self):
        #
        symbol_list = [
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
            Operator("+", None, None, "OPERATOR_PLUS", "+"),
            Constant("1", None, None, "RESERVED_TYPE_CHAR", 1),
            Operator("*", None, None, "OPERATOR_MULTIPLY", "*"),
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
        ]
        # (x > 5) and ('C' in {'A', 'B', 'C'})
        result = check_type_compatibility(symbol_list)
        self.assertFalse(result)

    def DONOTRUN_test_type_check_scenario_dual_levels_not_compatible_types(self):
        #
        symbol_list = [
            Constant("1", None, None, "UNSIGNED_REAL", 1),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            BooleanConstant.false(),
            +
            (
            BooleanConstant.false(),
            +
            Constant("1", None, None, "UNSIGNED_REAL", 1),
            )
        ]
        #
        result = check_type_compatibility(symbol_list)
        self.assertFalse(result)

"""
Identifier('V1'|RESERVED_TYPE_INTEGER|scenario_variable_declaration|0|V1|[]), 
Identifier('V2'|RESERVED_TYPE_INTEGER|scenario_variable_declaration|0|V2|[]), 
Identifier('_V3'|RESERVED_TYPE_REAL|scenario_variable_declaration|0|_V3|[]), 
Identifier('_V3_b'|RESERVED_TYPE_BOOLEAN|scenario_variable_declaration|0|_V3_b|[]), 
Identifier('_V3c'|RESERVED_TYPE_BYTE|scenario_variable_declaration|0|_V3c|[]), 
Identifier('_V3_d'|RESERVED_TYPE_CHAR|scenario_variable_declaration|0|_V3_d|[]), 
Identifier('_V3_e'|RESERVED_TYPE_STRING|scenario_variable_declaration|0|_V3_e|[]), 
Identifier('_V3_f'|RESERVED_TYPE_TEXT|scenario_variable_declaration|0|_V3_f|[]), 
Identifier('_V3g'|RESERVED_TYPE_WORD|scenario_variable_declaration|0|_V3g|[]), 
Identifier('_V3h'|RESERVED_TYPE_SET|scenario_variable_declaration|0|_V3h|[]), 
Identifier('V4'|^IDENTIFIER|scenario_variable_declaration|0|V4|[]), 
Identifier('V5'|^IDENTIFIER|scenario_variable_declaration|0|V5|[]), 
Identifier('V6'|^IDENTIFIER|scenario_variable_declaration|0|V6|[]), 
Identifier('V7'|^IDENTIFIER|scenario_variable_declaration|0|V7|[])]}
"""