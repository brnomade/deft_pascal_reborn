"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.abstract_emiter import CEmitter, CEmitter2, CMOCEmitter
from components.symbols.base_symbols import BaseSymbol, BaseKeyword, BaseType, BaseExpression
from components.symbols.operator_symbols import Operator, UnaryOperator
from components.symbols.type_symbols import PointerType, BasicType, StringType
from components.symbols.identifier_symbols import Identifier, PointerIdentifier, TypeIdentifier, ProcedureForwardIdentifier, ProcedureExternalIdentifier, ProcedureIdentifier
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
                         "PROCEDURE_DECLARATION",
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
            self._emiter = CEmitter2(token_list[1].value)
            #self._emiter = CEmitter(token_list[1].value)
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

        Example:
            Pascal
                CONST
                C1 = 'C';
                C5 = C1;
                C2 = 'C8C8C8C8';
                C6 = C2;

            C
                const char C1 = 'C';
                char C5;
                const char C2[81] = "C8C8C8C8";
                char C6[81];
                int main() {
                C5 = C1;
                strcpy(c6, c2);

        """
        # TODO: When managing procedure definitions, this code will need to adjust to emit at the correct level

        for token in token_list:
            assert token.category == "ConstantIdentifier", "ConstantIdentifier expected but found {0}".format(token)

            if token.value.cardinality > 1:
                self._log(WARNING, "Expression in constant declaration not yet supported and will be ignored. {0}".format(token))

            else:
                inner_type = token.type.type
                inner_c_type = token.type.type_to_c

                if inner_type in ["RESERVED_TYPE_STRING"]:
                    inner_literal = token.to_literal()
                    self._emiter.emit_constant_definition_part_string(token.name,
                                                                      inner_c_type,
                                                                      inner_literal.type.dimension,
                                                                      inner_literal.value_to_c)

                elif inner_type in ["RESERVED_TYPE_CHAR"]:
                    self._emiter.emit_constant_definition_part_char(token.name, inner_c_type)
                    self._expression(token.value)
                    self._emiter.emit_statement_terminator()

                elif inner_type in ["RESERVED_TYPE_POINTER"]:
                    self._emiter.emit_constant_definition_part_pointer(token.name, inner_c_type)
                    self._expression(token.value)
                    self._emiter.emit_statement_terminator()

                else:
                    self._emiter.emit_constant_definition_part_generic_left_side(token.name)
                    self._expression(token.value)
                    self._emiter.emit_constant_definition_part_generic_right_side()


    def _type_definition_part(self, token_list):
        """
        TYPE_DEFINITION_PART
        example: 'TYPE_DEFINITION_PART', 'token_list': [ TypeIdentifier(T6|BasicType(RESERVED_TYPE_INTEGER)),
                                                         TypeIdentifier(T7|BasicType(RESERVED_TYPE_REAL)),
                                                         TypeIdentifier(T8|BasicType(RESERVED_TYPE_CHAR)),
                                                         TypeIdentifier(T9|StringType(RESERVED_TYPE_STRING[80])),
                                                         TypeIdentifier(T10|BasicType(RESERVED_TYPE_BOOLEAN))
                                                       ]
        """
        for token in token_list:
            self._emiter.emit_type_definition()

            if isinstance(token.type, BasicType):
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
                self._emiter.emit_variable_declaration_part_generic(token.type.type_to_c, token.name)
            elif isinstance(token.type, StringType):
                self._emiter.emit_variable_declaration_part_string(token.type.type_to_c, token.name, token.type.dimension)
            elif isinstance(token.type, PointerType):
                self._emiter.emit_variable_declaration_part_pointer(token.type.type_to_c, token.name)
            else:
                line = "{0}".format(token)
                self._emiter.emit_header_line(line)


    def _variable_declaration_part(self, token_list):
        """
        VARIABLE_DECLARATION_PART
        example: 'VARIABLE_DECLARATION_PART', 'token_list': [ Identifier('V1'|BasicType(RESERVED_TYPE_INTEGER)|None),
                                                              Identifier('V2'|BasicType(RESERVED_TYPE_INTEGER)|None)
                                                            ]

        """
        for token in token_list:
            # TODO: Need to separate better the instances that are arriving here:
            # They could be Identifiers subclass? Currently a TypeIdentifier could be received
            # They could also be BaseTypes? Or specific Types like StringType and PointerType

            if isinstance(token, Identifier):
                if isinstance(token.type, StringType):
                    self._emiter.emit_variable_declaration_part_string(token.type.type_to_c, token.name, token.type.dimension)
                elif isinstance(token.type, TypeIdentifier):
                    self._emiter.emit_variable_declaration_part_generic(token.type.name, token.name)
                elif isinstance(token.type, PointerType):
                    self._emiter.emit_variable_declaration_part_pointer(token.type.type_to_c, token.name)
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
        # emit identifier
        identifier = input_list.pop(0)

        if isinstance(identifier.type, StringType):

            # discard operator ':='
            operator = input_list.pop(0)

            """
            scenarios of string assignment:
                1) string identifier <- expression of cardinality 1 [string literal]
                    pattern: char c[50] = "abcd";
                2) string identifier <- expression of cardinality 1 [string variable]
                    pattern: strcpy(str2, str1);
                3) string identifier <- expression of cardinality 2+ [string literals only and operators]
                    pattern: strcpy(variable, "abcd"); 
                             strcpy(variable, "defg");
                4) string identifier <- expression of cardinality 2+ [mixed string literals, operators and variables]
            """
            expression = input_list.pop(0)
            if expression.cardinality == 1 and expression.value[0].category.upper() == "STRINGLITERAL":
                # scenario 1
                self._emiter.emit_assignment_scenario_unary_string_literal(identifier.type.type_to_c,
                                                                           identifier.name,
                                                                           identifier.type.dimension,
                                                                           expression.value[0].value)
            elif expression.cardinality == 1 and expression.value[0].category.upper() == "IDENTIFIER":
                # scenario 2
                self._emiter.emit_assignment_scenario_unary_string_identifier(identifier.name,
                                                                              expression.value[0].name)
            else:
                # scenarios 3 and 4
                # the only operator valid for strings is '+' so the translation
                # to c does not take into account any other scenario.
                for e in expression.value:
                    if e.category.upper() == "STRINGLITERAL":
                        self._emiter.emit_assignment_scenario_multiple_string_literals(identifier.name, e.value)
                    elif e.category.upper() == "IDENTIFIER":
                        self._emiter.emit_assignment_scenario_unary_string_identifier(identifier.name, e.name)
                    elif not isinstance(e, Operator):
                        self._log(WARNING, "assignment_statement - emiter for '{0}' not yet implemented".format(e))

        else:

            if input_list[0].category == "UnaryOperator" and input_list[0].type == "OPERATOR_UPARROW":

                # if isinstance(identifier.type, PointerType):
                self._emiter.emit_assignment_pointer_left_side(identifier.name)

                # discard uparrow operator
                input_list.pop(0)

            else:
                self._emiter.emit_singleton(identifier.name)

            # emit operator ':='
            operator = input_list.pop(0)
            self._emiter.emit_singleton(operator.to_c)

            # emit expression
            self._expression(input_list.pop(0))

            # emit line terminator
            self._emiter.emit_statement_terminator()


    def _expression(self, a_generic_expression):
        # Process the incoming generic EXPRESSION
        assert isinstance(a_generic_expression, BaseExpression), a_generic_expression

        while a_generic_expression.value:
            token = a_generic_expression.value.pop(0)
            if isinstance(token, BaseKeyword):

                self._log(ERROR, "Incorrect keyword '{0}' received.".format(token))

            if isinstance(token, Operator):

                self._emiter.emit_operator_in_definition(token.to_c)

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
        #token = self._translate_operator_to_c(token)
        self._emiter.emit_closed_for_statement_control_variable(control_variable.name, token.to_c)

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
        input_list ->   [ ProcedureIdentifier('writeln'|RESERVED_TYPE_POINTER|None),
                          ActualParameter([StringLiteral('HELLO WORLD'|StringType(RESERVED_TYPE_STRING[80])|HELLO WORLD)]:None:None)
                        ]
        C syntax -> "printf"
        Pascal syntax -> write/writeln( A : B : C, ... ) :: A = value to print; B = field_width; C = decimal_field_width
        """
        identifier = input_list.pop(0)

        # self._emiter.emit("printf(")
        self._emiter.emit_procedure_call_write()

        for actual_parameter in input_list:

            if actual_parameter.cardinality == 3:
                action = self._emiter.emit_procedure_call_write_with_2_format
                # particle = "%*.*{0}\\t"
            elif actual_parameter.cardinality == 2:
                # particle = "%*{0}\\t"
                action = self._emiter.emit_procedure_call_write_with_1_format
            else:
                # particle = "%{0}\\t"
                action = self._emiter.emit_procedure_call_write_with_no_format

            if actual_parameter.value.type in ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_BOOLEAN"]:
                action("d")
            elif actual_parameter.value.type == "RESERVED_TYPE_REAL":
                action("f")
            elif actual_parameter.value.type in ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_TEXT"]:
                action("c")
            else:
                action("s")

        if identifier.name.upper() == "WRITELN":
            self._emiter.emit_procedure_call_write_format_close_with_new_line()
        else:
            self._emiter.emit_procedure_call_write_format_close()

        while True:
            actual_parameter = input_list.pop(0)

            if actual_parameter.cardinality == 3:
                field_width_expression = actual_parameter.field_width
                self._expression(field_width_expression)
                self._emiter.emit_procedure_call_parameter_separator()

                decimal_field_width_expression = actual_parameter.decimal_paces.value
                self._expression(decimal_field_width_expression)
                self._emiter.emit_procedure_call_parameter_separator()

            elif actual_parameter.cardinality == 2:
                field_width_expression = actual_parameter.field_width
                self._expression(field_width_expression)
                self._emiter.emit_procedure_call_parameter_separator()

            value_to_print_expression = actual_parameter.value
            self._expression(value_to_print_expression)

            if not input_list:
                break
            else:
                self._emiter.emit_procedure_call_parameter_separator()

        self._emiter.emit_procedure_call_closure()
        self._emiter.emit_statement_terminator()


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

                actual_parameter = input_list.pop(0)
                if actual_parameter.cardinality == 1:
                    self._expression(actual_parameter.value)
                else:
                    raise ValueError

                if input_list:
                    self._emiter.emit_procedure_call_parameter_separator()
                    # self._emiter.emit(", ")

            self._emiter.emit_procedure_call_closure()
            # self._emiter.emit_line(")")

    def _procedure_declaration(self, input_list):
        """
        'PROCEDURE_DECLARATION'
        input_list -> [ ProcedureIdentifier('first_procedure'|RESERVED_TYPE_POINTER|None)
                     ]
        Syntax: Pascal -> C
        return_type function_name( parameter list ) {
                                                        body of the function
                                                    }
        """
        token = input_list[0]
        if isinstance(token, ProcedureForwardIdentifier):
            self._emiter.emit_procedure_forward_declaration_left(token.name)
        elif isinstance(token, ProcedureExternalIdentifier):
            self._emiter.emit_procedure_external_declaration_left(token.name)
        else:
            self._emiter.emit_procedure_declaration_left(token.name)

        separator_counter = token.argument_counter - 1
        for argument in token.arguments:
            self._emiter.emit_procedure_declaration_argument(argument.type.type_to_c, argument.name)
            if separator_counter > 0:
                self._emiter.emit_procedure_declaration_argument_separator()
                separator_counter = separator_counter - 1

        if isinstance(token, ProcedureForwardIdentifier):
            self._emiter.emit_procedure_forward_declaration_right()
        elif isinstance(token, ProcedureExternalIdentifier):
            self._emiter.emit_procedure_external_declaration_right()
        else:
            self._emiter.emit_procedure_declaration_right()


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


