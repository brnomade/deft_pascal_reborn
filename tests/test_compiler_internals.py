from unittest import TestCase
from deft_pascal_compiler import DeftPascalCompiler
from symbol_table import BooleanConstant, Constant, Identifier, Operator
import logging

logger = logging.getLogger(__name__)


class TestCompilerInternals(TestCase):

    def test_type_check_scenario_assignment_unary_operation_compatible_type(self):

        compiler = DeftPascalCompiler()
        #
        symbol_list = [
            BooleanConstant.false(),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            Operator("NOT", None, None, "OPERATOR_NOT", "NOT"),
            BooleanConstant.false(),
        ]
        #
        result = compiler._check_type_compatibility_3(100,
                                                      "test_type_check_scenario_single_level_not_compatible_types",
                                                      symbol_list)

        self.assertTrue(result)

    def test_type_check_scenario_assignment_unary_operation_not_compatible_type(self):

        compiler = DeftPascalCompiler()
        #
        symbol_list = [
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            Operator("NOT", None, None, "OPERATOR_NOT", "NOT"),
            BooleanConstant.false(),
        ]
        #
        result = compiler._check_type_compatibility_3(100,
                                                      "test_type_check_scenario_single_level_not_compatible_types",
                                                      symbol_list)

        self.assertFalse(result)

    def test_type_check_scenario_expression_unary_operation_compatible_type(self):

        compiler = DeftPascalCompiler()
        #
        symbol_list = [
            Operator("NOT", None, None, "OPERATOR_NOT", "NOT"),
            BooleanConstant.false(),
        ]
        #
        result = compiler._check_type_compatibility_3(100,
                                                      "test_type_check_scenario_expression_unary_operation_compatible_type",
                                                      symbol_list)

        self.assertTrue(result)

    def test_type_check_scenario_expression_unary_operation_not_compatible_type(self):

        compiler = DeftPascalCompiler()
        #
        symbol_list = [
            Operator("NOT", None, None, "OPERATOR_NOT", "NOT"),
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
        ]
        #
        result = compiler._check_type_compatibility_3(100,
                  "test_type_check_scenario_expression_unary_operation_not_compatible_type",
                  symbol_list
                                                      )

        self.assertFalse(result)

    def test_type_check_scenario_assignment_single_level_not_compatible_types(self):

        compiler = DeftPascalCompiler()
        #
        symbol_list = [
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            BooleanConstant.false(),
        ]
        #
        result = compiler._check_type_compatibility_3(100,
                                                      "test_type_check_scenario_assignment_single_level_not_compatible_types",
                                                      symbol_list)

        self.assertFalse(result)

    def test_type_check_scenario_assignment_single_level_compatible_types(self):

        compiler = DeftPascalCompiler()
        #
        symbol_list = [
            BooleanConstant.true(),
            Operator(":=", None, None, "OPERATOR_ASSIGNMENT", ":="),
            BooleanConstant.false(),
        ]
        #
        result = compiler._check_type_compatibility_3(100,
                                                      "test_type_check_scenario_single_level_compatible_types",
                                                      symbol_list)

        self.assertTrue(result)

    def DONOTRUN_test_type_check_scenario_expression_single_level_compatible_types(self):

        compiler = DeftPascalCompiler()
        #
        symbol_list = [
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
            Operator("+", None, None, "OPERATOR_PLUS", "+"),
            Constant("1", None, None, "RESERVED_TYPE_CHAR", 1),
            Operator("*", None, None, "OPERATOR_MULTIPLY", "*"),
            Constant("1", None, None, "RESERVED_TYPE_INTEGER", 1),
        ]
        # (x > 5) and ('C' in {'A', 'B', 'C'})
        result = compiler._check_type_compatibility_3(100,
                                                      "test_type_check_scenario_single_level_not_compatible_types",
                                                      symbol_list)

        self.assertFalse(result)

    def DONOTRUN_test_type_check_scenario_dual_levels_not_compatible_types(self):

        compiler = DeftPascalCompiler()
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
        result = compiler._check_type_compatibility_3(100,
                                                      "test_type_check_scenario_single_level_not_compatible_types",
                                                      symbol_list)

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