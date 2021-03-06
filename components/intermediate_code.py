"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.abstract_emiter import CEmitter, CMOCEmitter
from components.symbols.base_symbols import BaseSymbol, BaseKeyword, BaseType, BaseExpression
from components.symbols.operator_symbols import Operator
from components.symbols.type_symbols import PointerType, BasicType, StringType
from components.symbols.identifier_symbols import Identifier, PointerIdentifier, ConstantIdentifier
from components.symbols.literals_symbols import Literal
from utils import compiler_utils
import logging
from logging import ERROR, WARNING, INFO
import copy


class IntermediateCode:

    _GLB_LOGGER = logging.getLogger("IntermediateCode")

    def __init__(self, cmoc=False, stack_size=1000):
        self._emiter = None
        self._target = None
        if cmoc:
            self._target = "CMOC"
        self._i_stack = [None] * stack_size
        self._top = 0
        self._temp_stack = []
        self._actions = {"PROGRAM_HEADING",
                         "CONSTANT_DEFINITION_PART",
                         "TYPE_DEFINITION_PART",
                         "VARIABLE_DECLARATION_PART",
                         "RESERVED_STRUCTURE_BEGIN_PROGRAM",
                         "RESERVED_STRUCTURE_END_PROGRAM",
                         "RESERVED_STRUCTURE_BEGIN_BLOCK",
                         "RESERVED_STRUCTURE_END_BLOCK",
                         "ASSIGNMENT_STATEMENT",
                         "EXPRESSION",
                         "REPEAT_STATEMENT",
                         "REPEAT_STATEMENT_UNTIL",
                         "CLOSED_FOR_STATEMENT",
                         "CLOSED_WHILE_STATEMENT",
                         "PROCEDURE_CALL",
                         "CLOSED_IF_STATEMENT",
                         "CLOSED_IF_STATEMENT_ELSE"
                         }

    def _log(self, log_type=INFO, log_info=""):
        if log_type == ERROR:
            self._GLB_LOGGER.error(log_info)
        elif log_type == WARNING:
            self._GLB_LOGGER.warning(log_info)
        elif log_type == INFO:
            self._GLB_LOGGER.info(log_info)
        else:
            self._GLB_LOGGER.debug(log_info)

    def __str__(self):
        my_representation = "\n\n{0}(".format(type(self).__name__)
        for i in range(0, self._top):
            my_representation += "\n"
            my_representation += str(self._i_stack[i])
        my_representation += "\n)\n"
        return my_representation

    def __repr__(self):
        my_representation = "\n\n{0}(".format(type(self).__name__)
        for i in range(0, self._top):
            my_representation += "\n"
            my_representation += str(self._i_stack[i])
        my_representation += "\n)\n"
        return my_representation

    def _advance_top(self):
        self._top += 1
        self._temp_stack = []

    # @staticmethod
    # def _translate_token_value_to_c(token):
    #     # translates a pascal symbol to c
    #     cvalue = token.value
    #     if token.type == "OPERATOR_ASSIGNMENT":
    #         token.value = "="
    #     elif token.type in ["RESERVED_TYPE_INTEGER"]:
    #         if "&B" in token.value.upper():     # == "NUMBER_BINARY"
    #             cvalue = "0b{0}".format(token.value.upper().strip("&B"))
    #         elif "&H" in token.value.upper():   # == "NUMBER_HEXADECIMAL"
    #             cvalue = "0x{0}".format(token.value.upper().strip("&H"))
    #         elif "&O" in token.value.upper():   # == "NUMBER_OCTAL"
    #             cvalue = "0{0}".format(token.value.upper().strip("&O"))
    #     elif token.type in ["CHARACTER", "STRING"]:
    #         cvalue = token.value.strip("'").strip('"')
    #     elif token.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
    #         cvalue = "true" if token.type == "CONSTANT_TRUE" else "false"
    #     elif token.type == "RESERVED_OPERATOR_AND":
    #         cvalue = "&&"
    #     else:
    #         print("Unknown type {0}".format(token))
    #     return cvalue

    def _translate_operator_to_c(self, in_token):
        token = copy.copy(in_token)
        #
        if token.type == "OPERATOR_ASSIGNMENT":

            token.value = "="

        elif token.type == "OPERATOR_AND":

            token.value = "&&"

        elif token.type == "OPERATOR_OR":

            token.value = "||"

        elif token.type == "OPERATOR_NOT":

            token.value = "!"

        elif token.type == "OPERATOR_NOT_EQUAL_TO":

            token.value = "!="

        elif token.type == "OPERATOR_EQUAL_TO":

            token.value = "=="

        elif token.type == "OPERATOR_DIV":

            token.value = "/"

        else:

            if token.type not in ["OPERATOR_PLUS", "OPERATOR_MULTIPLY", "OPERATOR_ARITHMETIC_NEGATION",
                                  "OPERATOR_DIVIDE", "OPERATOR_GREATER_THAN", "OPERATOR_GREATER_OR_EQUAL_TO"
                                  ]:    # this are the operators which are similar between pascal and c

                self._log(WARNING, "translation for operator '{0}' not yet implemented".format(token))

        return token

    # def _translate_type_to_c_type(self, in_token):
    #     token = copy.copy(in_token)
    #     #
    #     if token.type in ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING", "RESERVED_TYPE_TEXT"]:
    #
    #         token.type = "unsigned char"
    #
    #     elif token.type == "RESERVED_TYPE_INTEGER":
    #
    #         token.type = "int"
    #
    #     elif token.type == "RESERVED_TYPE_REAL":
    #
    #         token.type = "double"
    #
    #     elif token.type == "RESERVED_TYPE_BOOLEAN":
    #
    #         token.type = "_Bool"
    #
    #     else:
    #
    #         self._log(WARNING, "translation for operator '{0}' not yet implemented".format(token))
    #
    #     return token


    # def _translate_constant_to_c(self, in_token):
    #     token = copy.copy(in_token)
    #     #
    #     if token.type in ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"]:
    #
    #         token.type = "unsigned char"
    #         token.value = token.value.strip("'").strip('"')
    #
    #     elif token.type in ["STRING_VALUE"]:
    #
    #         raise NotImplementedError
    #
    #         # token.name = token.value.replace("'", '"')
    #         # token.type = "unsigned char"
    #         # token.value = token.value.strip("'").strip('"')
    #
    #     elif token.type == "RESERVED_TYPE_INTEGER":
    #
    #         if "&B" in token.value.upper():     # == "NUMBER_BINARY"
    #
    #             token.type = "unsigned short"
    #             token.value = "0b{0}".format(token.value.upper().strip("&B"))
    #
    #         elif "&H" in token.value.upper():   # == "NUMBER_HEXADECIMAL"
    #
    #             token.type = "unsigned short"
    #             token.value = "0x{0}".format(token.value.upper().strip("&H"))
    #
    #         elif "&O" in token.value.upper():   # == "NUMBER_OCTAL"
    #
    #             token.type = "unsigned short"
    #             token.value = "0{0}".format(token.value.upper().strip("&O"))
    #
    #         elif int(token.value) >= 0:         # == "UNSIGNED_DECIMAL"
    #
    #             token.type = "unsigned short"
    #
    #         else:
    #
    #             token.type = "short"
    #
    #     elif token.type == "RESERVED_TYPE_REAL":
    #
    #         token.type = "float"
    #
    #     elif token.type == "RESERVED_TYPE_BOOLEAN":
    #
    #         token.type = "bool"
    #         token.value = "true" if token.value else "false"
    #
    #         if token.name in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
    #             token.name = "true" if token.value else "false"
    #
    #     elif token.type == "RESERVED_TYPE_POINTER":
    #
    #         token.type = "int"
    #         token.value = "NULL"
    #
    #     else:
    #
    #         self._log(WARNING, "translation for constant '{0}' not yet implemented".format(token))
    #
    #     return token

    def init(self, action_name):
        self._i_stack[self._top] = {"action_name": action_name,
                                    "token_list": None
                                    }


    def push(self, an_input):
        if isinstance(an_input, list):
            self._temp_stack += an_input
        else:
            self._temp_stack.append(an_input)


    def flush(self):
        self._i_stack[self._top]["token_list"] = self._temp_stack
        self._advance_top()


    def generate(self):
        for i in range(0, self._top):
            #
            node = self._i_stack[i]
            token_list = node["token_list"]
            action_name = node["action_name"]
            #
            if action_name in self._actions:
                method_to_call = getattr(IntermediateCode, "_" + action_name.lower())
                method_to_call(self, token_list)
            else:
                self._log(ERROR, "action {0} - '{0}' not yet implemented".format(action_name, token_list))
            #
        return self._emiter.output_code


    def _program_heading(self, token_list):
        """
        PROGRAM_HEADING
        """
        if self._target == "CMOC":
            self._emiter = CMOCEmitter(token_list[1].value)
        else:
            self._emiter = CEmitter(token_list[1].value)
        self._emiter.emit_program_heading()


    def _constant_definition_part(self, token_list):
        """
        CONSTANT_DEFINITION_PART
        example:
        [ ConstantIdentifier('C1'|BasicType(RESERVED_TYPE_INTEGER)|GenericExpression('GENERIC_EXPRESSION'|BasicType(RESERVED_TYPE_INTEGER)|[NumericLiteral('&B00'|BasicType(RESERVED_TYPE_INTEGER)|&B00|[])]|[])|[]),
          ConstantIdentifier('C2'|BasicType(RESERVED_TYPE_INTEGER)|GenericExpression('GENERIC_EXPRESSION'|BasicType(RESERVED_TYPE_INTEGER)|[NumericLiteral('&b11'|BasicType(RESERVED_TYPE_INTEGER)|&b11|[])]|[])|[]),
          ConstantIdentifier('C1'|BasicType(RESERVED_TYPE_CHAR)|GenericExpression[StringLiteral('C')]),
          ConstantIdentifier('C3'|StringType(RESERVED_TYPE_STRING[80])|GenericExpression[StringLiteral('C')|BinaryOperator(OPERATOR_PLUS)|StringLiteral('B')]),
          ConstantIdentifier('C5'|StringType(RESERVED_TYPE_STRING[80])|GenericExpression[ConstantIdentifier(C1)|BinaryOperator(OPERATOR_PLUS)|ConstantIdentifier(C3)])
        ]
        """
        for token in token_list:
            assert token.category == "ConstantIdentifier", "ConstantIdentifier expected but found {0}".format(token)

            inner_type = token.type.type
            inner_c_type = token.type.type_to_c

            if inner_type in ["RESERVED_TYPE_STRING"]:
                inner_literal = token.to_literal()
                self._emiter.emit_constant_definition_part_string(token.name, inner_c_type, inner_literal.type.dimension, inner_literal.value_to_c)

            elif inner_type in ["RESERVED_TYPE_CHAR"]:
                self._emiter.emit_constant_definition_part_char(token.name, inner_c_type)
                self._expression(token.value)

            elif inner_type in ["RESERVED_TYPE_POINTER"]:
                self._emiter.emit_constant_definition_part_pointer(token.name, inner_c_type)
                self._expression(token.value)

            else:
                self._emiter.emit_constant_definition_part_generic(token.name, inner_c_type)
                self._expression(token.value)

            self._emiter.emit_statement_terminator()

    def _type_definition_part(self, token_list):
        """
        TYPE_DEFINITION_PART
        example: 'TYPE_DEFINITION_PART', 'token_list': [BasicType('T1'|RESERVED_TYPE_INTEGER|None|scenario_type_declaration_with_base_types|0|[]),
        """
        for token in token_list:
            if isinstance(token, BasicType):
                """
                typedef, can be used to give a type a new name. 
                example: typedef unsigned char BYTE;
                After this, the identifier BYTE can be used as an abbreviation for the type unsigned char
                Example:
                BYTE  b1, b2;
                By convention, uppercase letters are used for these definitions 
                Example for strings:
                typedef char ItemType[10];
                """
                if token.type in ["RESERVED_TYPE_STRING"]:
                    line = "typedef {0} {1}[ ];"
                else:
                    line = "typedef {0} {1};"
                # token = self._translate_type_to_c_type(token)
                self._emiter.emit_header_line(line.format(token.type.type_to_c, token.name))
            elif isinstance(token, PointerType):
                if token.type in ["RESERVED_TYPE_STRING"]:
                    line = "typedef {0} *{1}[ ];"
                else:
                    line = "typedef {0} *{1};"
                # token = self._translate_type_to_c_type(token)
                self._emiter.emit_header_line(line.format(token.type.type_to_c, token.name))


    def _variable_declaration_part(self, token_list):
        """
        VARIABLE_DECLARATION_PART
        example: 'VARIABLE_DECLARATION_PART', 'token_list': [ Identifier('V1'|BasicType(RESERVED_TYPE_INTEGER)|None),
                                                              Identifier('V2'|BasicType(RESERVED_TYPE_INTEGER)|None)
                                                            ]

        """
        for token in token_list:
            if isinstance(token, Identifier):
                if isinstance(token.type, StringType):
                    self._emiter.emit_variable_declaration_part_string(token.type.type_to_c, token.name, token.type.dimension)
                else:
                    self._emiter.emit_variable_declaration_part_generic(token.type.type_to_c, token.name)
            elif isinstance(token, PointerIdentifier):
                self._emiter.emit_variable_declaration_part_pointer(token.type.type_to_c, token.name)
            else:
                raise NotImplementedError

    def _reserved_structure_begin_program(self, token_list):
        """
        RESERVED_STRUCTURE_BEGIN_PROGRAM
        """
        self._emiter.emit_reserved_structure_begin_program()

    def _reserved_structure_begin_block(self, token_list):
        """
        RESERVED_STRUCTURE_BEGIN_BLOCK
        """
        self._emiter.emit_reserved_structure_begin_block()

    def _reserved_structure_end_program(self, token_list):
        """
        RESERVED_STRUCTURE_END_PROGRAM
        """
        self._emiter.emit_reserved_structure_end_program()

    def _reserved_structure_end_block(self, token_list):
        """
        RESERVED_STRUCTURE_END_BLOCK
        """
        self._emiter.emit_reserved_structure_end_block()

    def _assignment_statement(self, input_list):
        """
        ASSIGNMENT_STATEMENT
         emit assignment expressions
         input_list -> Identifier('fahren'|int|None|scenario_fahrenheit_to_celsius_converter|0|[]),
                       Operator(':='|OPERATOR_ASSIGNMENT|:=|scenario_fahrenheit_to_celsius_converter|0|[]),
                       GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant('0'|RESERVED_TYPE_INTEGER|0|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('+'|OPERATOR_PLUS|+|scenario_fahrenheit_to_celsius_converter|0|[]), Constant('1'|RESERVED_TYPE_INTEGER|1|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('+'|OPERATOR_PLUS|+|scenario_fahrenheit_to_celsius_converter|0|[]), Identifier('fahren'|int|None|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[])
        """

        """
        #include <stdio.h>
        #include <string.h>

        int main() {
            char str1[20] = "C programming";
            char str2[20];
            // copying str1 to str2
            strcpy(str2, str1);
        """

        # emit identifier
        identifier = input_list.pop(0)

        if identifier.type == "RESERVED_TYPE_STRING":

            self._emiter.emit_assignment_string_left_side(identifier.name)

            # discard operator ':='
            operator = input_list.pop(0)

            # emit expression
            self._expression(input_list.pop(0))

            # emit statement terminator
            self._emiter.emit_assignment_string_right_side()

        else:

            self._emiter.emit_singleton(identifier.name)

            # emit operator ':='
            operator = input_list.pop(0)
            operator = self._translate_operator_to_c(operator)
            self._emiter.emit_singleton(operator.value)

            # emit expression
            self._expression(input_list.pop(0))

            # emit line terminator
            self._emiter.emit_statement_terminator()


    def _expression(self, a_generic_expression):
        # Process the incoming generic EXPRESSION
        while a_generic_expression.value:
            token = a_generic_expression.value.pop(0)
            if isinstance(token, BaseKeyword):

                self._log(ERROR, "Incorrect keyword '{0}' received.".format(token))

            if isinstance(token, Operator):

                token = self._translate_operator_to_c(token)
                self._emiter.emit_singleton(token.value)

            elif isinstance(token, Literal):

                # token = self._translate_constant_to_c(token)
                # self._emiter.emit_singleton(token.name)
                self._emiter.emit_singleton(token.value_to_c)

            elif isinstance(token, Identifier):

                self._emiter.emit_singleton(token.name)

            elif isinstance(token, BaseSymbol):

                self._emiter.emit_singleton(token.name)

            else:

                self._log(WARNING, "expression action for token '{0}' not yet implemented".format(token))


    def _repeat_statement(self, input_list):
        """
        REPEAT_STATEMENT
        """
        self._emiter.emit_repeat_statement()

    def _repeat_statement_until(self, input_list):
        """
        REPEAT_STATEMENT_UNTIL
        input_list -> Keyword(until) GenericExpression(...)
        """
        if len(input_list) > 2:
            self._log(ERROR, "Unexpected expressions received in UNTIL statement. {0} ".format(input_list))
        #
        self._emiter.emit_repeat_statement_until()
        #
        self._expression(input_list[-1])
        #
        self._emiter.emit_repeat_statement_until_closure()

    def _closed_for_statement(self, input_list):
        """
        CLOSED_FOR_STATEMENT
        input_list -> Keyword(FOR) Identifier Operator(:=) Expression Keyword(TO/DOWNTO) Expression Keyword(DO)
        example ->  [[Keyword('for'|RESERVED_STATEMENT_FOR|for|scenario_fahrenheit_to_celsius_converter|0|[]),
                     Identifier('fahren'|int|None|scenario_fahrenheit_to_celsius_converter|0|[]),
                     Operator(':='|OPERATOR_ASSIGNMENT|:=|scenario_fahrenheit_to_celsius_converter|0|[]),
                     GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant('MIN'|unsigned int|32|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('+'|OPERATOR_PLUS|+|scenario_fahrenheit_to_celsius_converter|0|[]), Constant('5'|RESERVED_TYPE_INTEGER|5|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('-'|OPERATOR_MINUS|-|scenario_fahrenheit_to_celsius_converter|0|[]), Constant('10'|RESERVED_TYPE_INTEGER|10|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('*'|OPERATOR_MULTIPLY|*|scenario_fahrenheit_to_celsius_converter|0|[]), Constant('20'|RESERVED_TYPE_INTEGER|20|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[]),
                     Keyword('to'|RESERVED_STATEMENT_TO|to|scenario_fahrenheit_to_celsius_converter|0|[]),
                     GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant('MAX'|unsigned int|50|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[]),
                     Keyword('do'|RESERVED_STATEMENT_DO|do|scenario_fahrenheit_to_celsius_converter|0|[])]
                     ]
        Syntax: Pascal -> C
        for x := 1 to 10 do -> for ( x = 1 ; x <= 10 ; x = x + 1)
        for x := 10 downto 1 do -> for (x = 10; x >= 1 ; x = x - 1)
        """
        # process keyword 'for'
        token = input_list.pop(0)
        if not isinstance(token, BaseKeyword):
            self._log(ERROR, "Unknown symbol '{0}' received. Keyword expected.".format(token))

        # get control_variable
        control_variable = input_list.pop(0)

        # process operator ':='
        token = input_list.pop(0)
        if not isinstance(token, Operator):
            self._log(ERROR, "Unknown symbol '{0}' received. Operator expected.".format(token))

        # emit part of the for statement
        # self._emiter.emit("for ( {0} = ".format(control_variable.name))
        token = self._translate_operator_to_c(token)
        self._emiter.emit_closed_for_statement_control_variable(control_variable.name, token.value)

        # extract 'start_value' expression and send it to processing
        generic_expression = input_list.pop(0)
        self._expression(generic_expression)

        # process keyword 'to' or 'downto' - first part
        token = input_list.pop(0)
        if not isinstance(token, BaseKeyword):
            self._log(ERROR, "Unknown symbol '{0}' received. Keyword expected.".format(token))
        direction = token.type == "RESERVED_STATEMENT_TO"
        if direction:
            self._emiter.emit_closed_for_statement_to(control_variable.name)
            # self._emiter.emit(" ; {0} <= ".format(control_variable.name))
        else:
            self._emiter.emit_closed_for_statement_downto(control_variable.name)
            # self._emiter.emit(" ; {0} >= ".format(control_variable.name))

        # extract 'end_value' expression and send it to processing
        generic_expression = input_list.pop(0)
        self._expression(generic_expression)

        # process keyword 'to' or 'downto' - final part
        if direction:
            self._emiter.emit_closed_for_statement_step_upward(control_variable.name)
            # self._emiter.emit_line("; {0} = {0} + 1 )".format(control_variable.name))
        else:
            self._emiter.emit_closed_for_statement_step_downward(control_variable.name)
            # self._emiter.emit_line("; {0} = {0} - 1 )".format(control_variable.name))

    def _closed_while_statement(self, input_list):
        """
        CLOSED_WHILE_STATEMENT
        input_list -> Keyword(WHILE) Expression Keyword(DO)
        example ->  [Keyword('while'|RESERVED_STATEMENT_WHILE|while|scenario_fahrenheit_to_celsius_converter|0|[]),
                     GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant('LOOP'|unsigned int|3|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('<'|OPERATOR_LESS_THEN|<|scenario_fahrenheit_to_celsius_converter|0|[]), Constant('10'|RESERVED_TYPE_INTEGER|10|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[])
                    Keyword('DO'|RESERVED_STATEMENT_DO|DO|scenario_fahrenheit_to_celsius_converter|0|[])
                    ]
        Syntax: Pascal -> C
        while x > 1 do -> while ( x > 1 )
        """
        # process keyword 'while'
        token = input_list.pop(0)
        if not isinstance(token, BaseKeyword):
            self._log(ERROR, "Unknown symbol '{0}' received. Keyword expected.".format(token))

        self._emiter.emit_closed_while_statement()

        # extract expression and send it to processing
        generic_expression = input_list.pop(0)
        self._expression(generic_expression)

        # process keyword 'do'
        self._emiter.emit_closed_while_statement_do()


    def _procedure_call_write(self, input_list):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        input_list ->  [ProcedureIdentifier('writeln'|RESERVED_TYPE_POINTER|writeln|scenario_fahrenheit_to_celsius_converter|0|[]),
                        GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant(''Fahrenheit     Celsius''|STRING_VALUE|'Fahrenheit     Celsius'|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[]),
                        GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant(''another''|STRING_VALUE|'another'|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[])
                        ]
        C syntax -> "printf"
        Pascal syntax -> write/writeln( A : B : C, ... ) :: A = value to print; B = field_width; C = decimal_field_width
        """
        identifier = input_list.pop(0)

        # self._emiter.emit("printf(")
        self._emiter.emit_procedure_call_write()

        for token in input_list:
            format_counter = 2 - token.value.count(None)
            #
            if format_counter == 2:
                action = self._emiter.emit_procedure_call_write_with_2_format
                # particle = "%*.*{0}\\t"
            elif format_counter == 1:
                # particle = "%*{0}\\t"
                action = self._emiter.emit_procedure_call_write_with_1_format
            else:
                # particle = "%{0}\\t"
                action = self._emiter.emit_procedure_call_write_with_no_format
            #
            if token.type == "RESERVED_TYPE_INTEGER":
                action("d")
            elif token.type == "RESERVED_TYPE_REAL":
                action("f")
            else:
                action("s")
        #
        if identifier.name.upper() == "WRITELN":
            self._emiter.emit_procedure_call_write_format_close_with_new_line()
            # self._emiter.emit('\\n", ')
        else:
            self._emiter.emit_procedure_call_write_format_close()
            # self._emiter.emit('", ')
        #
        while True:
            token = input_list.pop(0)
            #
            value_to_print_stack = token.value[0]
            field_width_stack = token.value[1]
            decimal_field_width_stack = token.value[2]
            #
            format_counter = 2 - token.value.count(None)
            #
            if format_counter == 2:
                self._expression(field_width_stack)
                self._emiter.emit_procedure_call_parameter_separator()
                # self._emiter.emit(", ")
                self._expression(decimal_field_width_stack)
                self._emiter.emit_procedure_call_parameter_separator()
                # self._emiter.emit(", ")
            elif format_counter == 1:
                self._expression(field_width_stack)
                self._emiter.emit_procedure_call_parameter_separator()
                # self._emiter.emit(", ")
            #
            self._expression(value_to_print_stack)
            #
            if not input_list:
                break
            else:
                self._emiter.emit_procedure_call_parameter_separator()
                # self._emiter.emit(", ")

        self._emiter.emit_procedure_call_closure()
        self._emiter.emit_statement_terminator()
        # self._emiter.emit_line(") ;")


    def _procedure_call(self, input_list):
        """
         PROCEDURE_CALL
        input_list ->  [ProcedureIdentifier('writeln'|RESERVED_TYPE_POINTER|writeln|scenario_fahrenheit_to_celsius_converter|0|[]),
                        GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant(''Fahrenheit     Celsius''|STRING_VALUE|'Fahrenheit     Celsius'|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[]),
                        GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant(''another''|STRING_VALUE|'another'|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[])
                        ]
                        [ProcedureIdentifier('writeln'|RESERVED_TYPE_POINTER|writeln|scenario_fahrenheit_to_celsius_converter|0|[]),
                        GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|(
                                                        [Constant('MIN'|unsigned int|32|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('+'|OPERATOR_PLUS|+|scenario_fahrenheit_to_celsius_converter|0|[]), Constant('MAX'|unsigned int|50|scenario_fahrenheit_to_celsius_converter|0|[])], [Constant('10'|RESERVED_TYPE_INTEGER|10|scenario_fahrenheit_to_celsius_converter|0|[])])|None|None|[]), GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|([Constant('MAX'|unsigned int|50|scenario_fahrenheit_to_celsius_converter|0|[])], [Constant('10'|RESERVED_TYPE_INTEGER|10|scenario_fahrenheit_to_celsius_converter|0|[])])|None|None|[]), GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|([Constant('MIN'|unsigned int|32|scenario_fahrenheit_to_celsius_converter|0|[])], [Constant('10'|RESERVED_TYPE_INTEGER|10|scenario_fahrenheit_to_celsius_converter|0|[])])|None|None|[])]
        C syntax -> "printf"
        """
        token = input_list[0]
        if token.name.upper() in ["WRITE", "WRITELN"]:

            self._procedure_call_write(input_list)

        else:

            procedure_identifier = input_list.pop(0)
            self._emiter.emit_procedure_call(procedure_identifier.name)
            # self._emiter.emit("{0}(".format(procedure_identifier.name))

            while input_list:

                generic_expression = input_list.pop(0)
                if len(generic_expression.value) == 1:
                    parameter = generic_expression.value[0]
                    self._expression(parameter)
                else:
                    raise ValueError

                if input_list:
                    self._emiter.emit_procedure_call_parameter_separator()
                    # self._emiter.emit(", ")

            self._emiter.emit_procedure_call_closure()
            # self._emiter.emit_line(")")

    def _closed_if_statement(self, input_list):
        """
        CLOSED_if_STATEMENT
        input_list -> Keyword(IF) Expression Keyword(THEN)
        example ->  [Keyword('if'|RESERVED_STATEMENT_IF|if|scenario_fahrenheit_to_celsius_converter|0|[]),
                    GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant('LOOP'|RESERVED_TYPE_INTEGER|3|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('>'|OPERATOR_GREATER_THEN|>|scenario_fahrenheit_to_celsius_converter|0|[]), Constant('10'|RESERVED_TYPE_INTEGER|10|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[]),
                    Keyword('then'|RESERVED_STATEMENT_THEN|then|scenario_fahrenheit_to_celsius_converter|0|[])]
        Syntax: Pascal -> C
        if LOOP > 10 then -> if ( LOOP > 10 )
        """
        # process keyword 'if'
        token = input_list.pop(0)
        if not isinstance(token, BaseKeyword):
            self._log(ERROR, "Unknown symbol '{0}' received. Keyword expected.".format(token))
        self._emiter.emit_closed_if_statement()

        # extract 'expression'  and send it to processing
        generic_expression = input_list.pop(0)
        self._expression(generic_expression)

        # process keyword 'then'
        token = input_list.pop(0)
        if not isinstance(token, BaseKeyword):
            self._log(ERROR, "Unknown symbol '{0}' received. Keyword expected.".format(token))
        self._emiter.emit_closed_if_statement_then()


    def _closed_if_statement_else(self, input_list):
        """
        CLOSED_if_STATEMENT_ELSE
        input_list -> Keyword(ELSE)
        example -> [Keyword('else'|RESERVED_STATEMENT_ELSE|else|scenario_fahrenheit_to_celsius_converter|0|[])
                   ]
        """
        # process keyword 'ELSE'
        token = input_list.pop(0)
        if not isinstance(token, BaseKeyword):
            self._log(ERROR, "Unknown symbol '{0}' received. Keyword expected.".format(token))
        self._emiter.emit_closed_if_statement_else()


