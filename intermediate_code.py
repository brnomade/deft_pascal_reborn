from abstract_emiter import CEmitter
from symbols import Operator, Constant, Identifier, Keyword, PointerIdentifier, ProcedureIdentifier, BasicType, PointerType, GenericExpression
import logging
from logging import ERROR, WARNING, INFO

logger = logging.getLogger(__name__)

_GLB_STACK_SIZE = 1000


class IntermediateCode:

    def __init__(self):
        self._i_stack = [None] * _GLB_STACK_SIZE
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
                         "CLOSED_FOR_STATEMENT",
                         "PROCEDURE_CALL"
                         }

    def _log(self, log_type=INFO, log_info=""):
        if log_type == ERROR:
            logger.error(log_info)
        elif log_type == WARNING:
            logger.warning(log_info)
        else:
            logger.info(log_info)

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

    @staticmethod
    def _translate_token_value_to_c(token):
        # translates a pascal symbol to c
        cvalue = token.value
        if token.type == "OPERATOR_ASSIGNMENT":
            token.value = "="
        elif token.type in ["RESERVED_TYPE_INTEGER"]:
            if "&B" in token.value.upper():     # == "NUMBER_BINARY"
                cvalue = "0b{0}".format(token.value.upper().strip("&B"))
            elif "&H" in token.value.upper():   # == "NUMBER_HEXADECIMAL"
                cvalue = "0x{0}".format(token.value.upper().strip("&H"))
            elif "&O" in token.value.upper():   # == "NUMBER_OCTAL"
                cvalue = "0{0}".format(token.value.upper().strip("&O"))
        elif token.type in ["CHARACTER", "STRING"]:
            cvalue = token.value.strip("'").strip('"')
        elif token.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
            cvalue = "true" if token.type == "CONSTANT_TRUE" else "false"
        elif token.type == "RESERVED_OPERATOR_AND":
            cvalue = "&&"
        return cvalue

    @staticmethod
    def _translate_operator_token_to_c(token):
        # translates a pascal operator to c
        if token.type == "OPERATOR_ASSIGNMENT":
            token.value = "="
        elif token.type == "RESERVED_OPERATOR_AND":
            token.value = "&&"

    @staticmethod
    def _translate_identifier_token_to_c(token):
        if token.type in ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING", "RESERVED_TYPE_TEXT"]:
            token.type = "unsigned char"
        elif token.type == "RESERVED_TYPE_INTEGER":
            token.type = "int"
        elif token.type == "RESERVED_TYPE_REAL":
            token.type = "float"
        elif token.type == "RESERVED_TYPE_BOOLEAN":
            token.type = "_Bool"

    @staticmethod
    def _translate_constant_token_to_c(token):
        z = 1
        if token.type in ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"]:
            token.type = "unsigned char"
            token.value = token.value.strip("'").strip('"')
        elif token.type in ["STRING_VALUE"]:
            token.name = token.value.replace("'", '"')
            token.type = "unsigned char"
            token.value = token.value.strip("'").strip('"')
        elif token.type == "RESERVED_TYPE_INTEGER":
            if "&B" in token.value.upper():     # == "NUMBER_BINARY"
                token.type = "unsigned short"
                token.value = "0b{0}".format(token.value.upper().strip("&B"))
            elif "&H" in token.value.upper():   # == "NUMBER_HEXADECIMAL"
                token.type = "unsigned short"
                token.value = "0x{0}".format(token.value.upper().strip("&H"))
            elif "&O" in token.value.upper():   # == "NUMBER_OCTAL"
                token.type = "unsigned short"
                token.value = "0{0}".format(token.value.upper().strip("&O"))
            elif int(token.value) >= 0:         # == "UNSIGNED_DECIMAL"
                token.type = "unsigned int"
            else:
                token.type = "int"
        elif token.type == "RESERVED_TYPE_REAL":
            token.type = "float"
        elif token.type == "RESERVED_TYPE_BOOLEAN":
            token.type = "_Bool"
            token.value = "true" if token.type == "CONSTANT_TRUE" else "false"
        elif token.type == "RESERVED_TYPE_POINTER":
            token.type = "int"
            token.value = "NULL"
        else:
            print("Unknown type {0}".format(token))
        z = 2

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

            node = self._i_stack[i]
            token_list = node["token_list"]
            action_name = node["action_name"]

            if action_name in self._actions:
                method_to_call = getattr(IntermediateCode, "_" + action_name.lower())
                method_to_call(self, token_list)
            else:
                self._log(ERROR, "action {0} - '{0}' not yet implemented".format(action_name, token_list))

        self._emiter.write_file()


    def _program_heading(self, token_list):
        """
        PROGRAM_HEADING
        """
        self._emiter = CEmitter(token_list[1].value)
        self._emiter.emit_header_line("#include <stdio.h>")
        self._emiter.emit_header_line("#include <stdbool.h>")

    def _constant_definition_part(self, token_list):
        """
        CONSTANT_DEFINITION_PART
        example: 'CONSTANT_DEFINITION_PART', 'token_list': [Constant('C1'|RESERVED_TYPE_INTEGER|2|scenario_constant_declaration|0|[])
        """
        for token in token_list:
            if isinstance(token, Constant):
                if token.type in ["RESERVED_TYPE_STRING"]:
                    line = "const {0} {1} [ ] = \"{2}\";"
                elif token.type in ["RESERVED_TYPE_CHAR"]:
                    line = "const {0} {1} = '{2}';"
                elif token.type in ["RESERVED_TYPE_POINTER"]:
                    line = "const {0} *{1} = {2};"
                else:
                    line = "const {0} {1} = {2};"
                self._translate_constant_token_to_c(token)
                self._emiter.emit_header_line(line.format(token.type, token.name, token.value))


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
                self._translate_identifier_token_to_c(token)
                self._emiter.emit_header_line(line.format(token.type, token.name))
            elif isinstance(token, PointerType):
                if token.type in ["RESERVED_TYPE_STRING"]:
                    line = "typedef {0} *{1}[ ];"
                else:
                    line = "typedef {0} *{1};"
                self._translate_identifier_token_to_c(token)
                self._emiter.emit_header_line(line.format(token.type, token.name))


    def _variable_declaration_part(self, token_list):
        """
        VARIABLE_DECLARATION_PART
        example: 'VARIABLE_DECLARATION_PART', 'token_list': [Identifier('V1' | RESERVED_TYPE_INTEGER | None | scenario_variable_declaration_with_base_types | 0 | []),
        """
        for token in token_list:
            if isinstance(token, Identifier):
                if token.type in ["RESERVED_TYPE_STRING"]:
                    line = "{0} {1} [ ];"
                else:
                    line = "{0} {1};"
                self._translate_identifier_token_to_c(token)
                self._emiter.emit_header_line(line.format(token.type, token.name))
            elif isinstance(token, PointerIdentifier):
                """
                type *var-name;
                type is the pointer's base type; it must be a valid C data type 
                var-name is the name of the pointer variable. 
                The asterisk * used to declare a pointer. 
                Examples:
                    int    *ip;    /* pointer to an integer */
                    double *dp;    /* pointer to a double */
                    float  *fp;    /* pointer to a float */
                    char   *ch     /* pointer to a character */
                """
                line = "{0} *{1};"
                self._translate_identifier_token_to_c(token)
                self._emiter.emit_header_line(line.format(token.type, token.name))


    def _reserved_structure_begin_program(self, token_list):
        """
        RESERVED_STRUCTURE_BEGIN_PROGRAM
        """
        self._emiter.emit_line("int main() {")

    def _reserved_structure_begin_block(self, token_list):
        """
        RESERVED_STRUCTURE_BEGIN_BLOCK
        """
        self._emiter.emit_line("{")

    def _reserved_structure_end_program(self, token_list):
        """
        RESERVED_STRUCTURE_END_PROGRAM
        """
        self._emiter.emit_line("return 0; \n }")

    def _reserved_structure_end_block(self, token_list):
        """
        RESERVED_STRUCTURE_END_BLOCK
        """
        self._emiter.emit_line("}")

    def _assignment_statement(self, input_list):
        """
        ASSIGNMENT_STATEMENT
         emit assignment expressions
         input_list -> Identifier('fahren'|int|None|scenario_fahrenheit_to_celsius_converter|0|[]),
                       Operator(':='|OPERATOR_ASSIGNMENT|:=|scenario_fahrenheit_to_celsius_converter|0|[]),
                       GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant('0'|RESERVED_TYPE_INTEGER|0|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('+'|OPERATOR_PLUS|+|scenario_fahrenheit_to_celsius_converter|0|[]), Constant('1'|RESERVED_TYPE_INTEGER|1|scenario_fahrenheit_to_celsius_converter|0|[]), Operator('+'|OPERATOR_PLUS|+|scenario_fahrenheit_to_celsius_converter|0|[]), Identifier('fahren'|int|None|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[])
        """

        particle = "{0}"

        # emit identifier
        identifier = input_list.pop(0)
        self._emiter.emit(particle.format(identifier.name))

        # emit operator ':='
        operator = input_list.pop(0)
        self._translate_operator_token_to_c(operator)
        self._emiter.emit(particle.format(operator.value))

        # emit expression
        self._expression(input_list.pop(0))

        self._emiter.emit_line(";")


    def _expression(self, a_generic_expression):
        # EXPRESSION

        while a_generic_expression.value:
            token = a_generic_expression.value.pop(0)
            particle = "{0} "
            if isinstance(token, Keyword):
                self._log(ERROR, "Unknown keyword '{0}' received.".format(token))
            if isinstance(token, Operator):
                if token.type == "OPERATOR_MINUS":
                    particle = "{0}"
                self._translate_operator_token_to_c(token)
                self._emiter.emit(particle.format(token.value))
            elif isinstance(token, Constant):
                self._translate_constant_token_to_c(token)
                self._emiter.emit(particle.format(token.name))
            elif isinstance(token, Identifier):
                self._emiter.emit(particle.format(token.name))
            elif isinstance(token, PointerIdentifier):
                raise NotImplementedError
            elif isinstance(token, ProcedureIdentifier):
                raise NotImplementedError
            else:
                self._emiter.emit(particle.format(token.name))


    def _repeat_statement(self, token_list):
        # REPEAT_STATEMENT
        self._emiter.emit_action_8(token_list)


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
        if not isinstance(token, Keyword):
            self._log(ERROR, "Unknown symbol '{0}' received. Keyword expected.".format(token))

        # get control_variable
        control_variable = input_list.pop(0)

        # process operator ':='
        token = input_list.pop(0)
        if not isinstance(token, Operator):
            self._log(ERROR, "Unknown symbol '{0}' received. Operator expected.".format(token))

        # emit part of the for statement
        self._emiter.emit("for ( {0} = ".format(control_variable.name))

        # extract 'start_value' expression and send it to processing
        generic_expression = input_list.pop(0)
        self._expression(generic_expression)

        # process keyword 'to' or 'downto' - first part
        token = input_list.pop(0)
        if not isinstance(token, Keyword):
            self._log(ERROR, "Unknown symbol '{0}' received. Keyword expected.".format(token))
        direction = token.type == "RESERVED_STATEMENT_TO"
        if direction:
            self._emiter.emit(" ; {0} <= ".format(control_variable.name))
        else:
            self._emiter.emit(" ; {0} >= ".format(control_variable.name))

        # extract 'end_value' expression and send it to processing
        generic_expression = input_list.pop(0)
        self._expression(generic_expression)

        # process keyword 'to' or 'downto' - final part
        if direction:
            self._emiter.emit_line("; {0} = {0} + 1 )".format(control_variable.name))
        else:
            self._emiter.emit_line("; {0} = {0} - 1 )".format(control_variable.name))


    def _procedure_call_emit_write(self, input_list):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        input_list ->  [ProcedureIdentifier('writeln'|RESERVED_TYPE_POINTER|writeln|scenario_fahrenheit_to_celsius_converter|0|[]),
                        GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant(''Fahrenheit     Celsius''|STRING_VALUE|'Fahrenheit     Celsius'|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[]),
                        GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[Constant(''another''|STRING_VALUE|'another'|scenario_fahrenheit_to_celsius_converter|0|[])]|None|None|[])
                        ]
        C syntax -> "printf"
        Pascal syntax -> write/writeln( A : B : C, ... ) :: A = value to print; B = field_width; C = decimal_field_width
        """
        token = input_list.pop(0)

        self._emiter.emit('printf("')

        for token in input_list:
            format_counter = 2 - token.value.count(None)
            #
            if format_counter == 2:
                particle = "%*.*{0}\\t "
            elif format_counter == 1:
                particle = "%*{0}\\t "
            else:
                particle = "%{0}\\t "
            #
            if token.type == "RESERVED_TYPE_INTEGER":
                self._emiter.emit(particle.format("d"))
            elif token.type == "RESERVED_TYPE_REAL":
                self._emiter.emit(particle.format("f"))
            else:
                self._emiter.emit(particle.format("s"))

        if token.name.upper() == "WRITELN":
            self._emiter.emit('\\n", ')
        else:
            self._emiter.emit('", ')

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
                self._emiter.emit(", ")
                self._expression(decimal_field_width_stack)
                self._emiter.emit(", ")
            elif format_counter == 1:
                self._expression(field_width_stack)
                self._emiter.emit(", ")
            #
            self._expression(value_to_print_stack)
            #
            if not input_list:
                break
            else:
                self._emiter.emit(", ")

        self._emiter.emit_line(") ;")


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

            self._procedure_call_emit_write(input_list)

        else:

            procedure_identifier = input_list.pop(0)
            self._emiter.emit("{0}(".format(procedure_identifier.name))

            while input_list:

                generic_expression = input_list.pop(0)
                if len(generic_expression.value) == 1:
                    parameter = generic_expression.value[0]
                    self._expression(parameter)
                else:
                    raise ValueError

                if input_list:
                    self._emiter.emit(", ")

            self._emiter.emit_line(")")
