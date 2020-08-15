"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
VERSION.......: 0.1
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

import os
import logging


class AbstractEmitter:

    logging.basicConfig()
    _GLB_LOGGER = logging.getLogger("AbstractEmitter")

    def __init__(self, file_name, dir_path="output\\sources"):

        path = os.getcwd()
        self.full_path = os.path.join(path, dir_path, file_name + ".c")
        self.header = ""
        self.code = ""

    def emit(self, input_source):
        self.code += input_source

    def emit_line(self, input_source):
        self.code += input_source + '\n'

    def emit_header(self, input_source):
        self.code += input_source

    def emit_header_line(self, input_source):
        self.header += input_source + '\n'

    @property
    def output_code(self):
        return self.header + self.code

    def write_file(self):
        with open(self.full_path, 'w') as outputFile:
            outputFile.write(self.header + self.code)


class CEmitter(AbstractEmitter):

    def emit_singleton(self, a_generic_string):
        """
        Just emits a single input string
        """
        particle = "{0}"
        self.emit(particle.format(a_generic_string))

    def emit_singleton_line(self, a_generic_string):
        """
        Just emits a single input string
        """
        particle = "{0}"
        self.emit_line(particle.format(a_generic_string))

    def emit_program_heading(self):
        """
        PROGRAM_HEADING
        """
        self.emit_header_line("#include <stdio.h>")
        self.emit_header_line("#include <stdbool.h>")

    def emit_constant_definition_part_string(self, in_name, in_type, in_value):
        """
        CONSTANT_DEFINITION_PART
        """
        line = "const {0} {1} [255] = \"{2}\";"
        self.emit_header_line(line.format(in_type, in_name, in_value))

    def emit_constant_definition_part_char(self, in_name, in_type, in_value):
        """
        CONSTANT_DEFINITION_PART
        const type variable = value;
        """
        line = "const {0} {1} = '{2}';"
        self.emit_header_line(line.format(in_type, in_name, in_value))

    def emit_constant_definition_part_pointer(self, in_name, in_type, in_value):
        """
        CONSTANT_DEFINITION_PART
        const type variable = value;
        """
        line = "const {0} *{1} = {2};"
        self.emit_header_line(line.format(in_type, in_name, in_value))

    def emit_constant_definition_part_generic(self, in_name, in_type, in_value):
        """
        CONSTANT_DEFINITION_PART
        const type variable = value;
        """
        line = "const {0} {1} = {2};"
        self.emit_header_line(line.format(in_type, in_name, in_value))

    def emit_variable_declaration_part_string(self, in_type, in_name):
        """
        VARIABLE_DECLARATION_PART
        """
        line = "{0} {1} [ ];"
        self.emit_header_line(line.format(in_type, in_name))

    def emit_variable_declaration_part_pointer(self, in_type, in_name):
        """
        VARIABLE_DECLARATION_PART
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
        self.emit_header_line(line.format(in_type, in_name))

    def emit_variable_declaration_part_generic(self, in_type, in_name):
        """
        VARIABLE_DECLARATION_PART
        """
        line = "{0} {1};"
        self.emit_header_line(line.format(in_type, in_name))

    def emit_reserved_structure_begin_program(self):
        """
        RESERVED_STRUCTURE_BEGIN_PROGRAM
        """
        line = "int main() {"
        self.emit_line(line)

    def emit_reserved_structure_begin_block(self):
        """
        RESERVED_STRUCTURE_BEGIN_BLOCK
        """
        particle = " {"
        self.emit_singleton_line(particle)

    def emit_reserved_structure_end_program(self):
        """
        RESERVED_STRUCTURE_END_PROGRAM
        """
        line = "return 0; \n }"
        self.emit_line(line)

    def emit_reserved_structure_end_block(self):
        """
        RESERVED_STRUCTURE_END_BLOCK
        """
        particle = "}"
        self.emit_singleton_line(particle)

    def emit_statement_terminator(self):
        """
        STATEMENT_TERMINATOR
        """
        particle = ";"
        self.emit_line(particle)

    def emit_closed_for_statement_control_variable(self, in_variable, in_operator):

        particle = "for ({0} {1} "
        self.emit(particle.format(in_variable, in_operator))

    def emit_closed_for_statement_to(self, in_variable):

        particle = " ; {0} <= "
        self.emit(particle.format(in_variable))

    def emit_closed_for_statement_downto(self, in_variable):

        particle = " ; {0} >= "
        self.emit(particle.format(in_variable))

    def emit_closed_for_statement_step_upward(self, in_variable):

        particle = "; {0} = {0} + 1)"
        self.emit(particle.format(in_variable))

    def emit_closed_for_statement_step_downward(self, in_variable):

        particle = "; {0} = {0} - 1)"
        self.emit(particle.format(in_variable))

    def emit_closed_while_statement(self):

        particle = "while ("
        self.emit(particle)

    def emit_closed_while_statement_do(self):

        particle = ")"
        self.emit_singleton(particle)

    def emit_procedure_call(self, in_procedure_name):
        """
         PROCEDURE_CALL
        """
        particle = "{0}("
        self.emit(particle.format(in_procedure_name))

    def emit_procedure_call_parameter_separator(self):
        line = ","
        self.emit_singleton(line)

    # def emit_separator(self):
    #    line = ","
    #    self.emit_singleton(line)

    def emit_procedure_call_closure(self):
        """
         PROCEDURE_CALL
        """
        particle = ")"
        self.emit_singleton(particle)

    def emit_procedure_call_write(self):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        """
        particle = 'printf("'
        self.emit(particle)

    def emit_procedure_call_write_format_close_with_new_line(self):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        """
        particle = '\\n", '
        self.emit(particle)

    def emit_procedure_call_write_format_close(self):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        """
        particle = '", '
        self.emit(particle)

    def emit_procedure_call_write_with_2_format(self, data_type_indicator):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        2 formatting particles
        """
        particle = "%*.*{0}\\t"
        self.emit(particle.format(data_type_indicator))

    def emit_procedure_call_write_with_1_format(self, data_type_indicator):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        2 formatting particles
        """
        particle = "%*{0}\\t"
        self.emit(particle.format(data_type_indicator))

    def emit_procedure_call_write_with_no_format(self, data_type_indicator):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        2 formatting particles
        """
        particle = "%{0}\\t"
        self.emit(particle.format(data_type_indicator))

    def emit_repeat_statement(self):
        line = "do {"
        self.emit_line(line)

    def emit_repeat_statement_until(self):
        particle = "} while (!("
        self.emit(particle)

    def emit_repeat_statement_until_closure(self):
        line = "));"
        self.emit_line(line)

    def emit_closed_if_statement(self):
        particle = "if ("
        self.emit(particle)

    def emit_closed_if_statement_then(self):
        particle = ")"
        self.emit_line(particle)

    def emit_closed_if_statement_else(self):
        particle = "else"
        self.emit_line(particle)

# @staticmethod
    # def _translate_token_value_to_c(a_token):
    #     # translates a pascal symbol to c
    #     if a_token.type == "OPERATOR_ASSIGNMENT":
    #         cvalue = "="
    #     elif a_token.type in ["CHARACTER", "STRING"]:
    #         cvalue = a_token.value.strip("'").strip('"')
    #     elif a_token.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
    #         cvalue = "true" if a_token.type == "CONSTANT_TRUE" else "false"
    #     elif a_token.type == "NUMBER_HEXADECIMAL":
    #         cvalue = "0x{0}".format(a_token.value.upper().strip("&H"))
    #     elif a_token.type == "NUMBER_OCTAL":
    #         cvalue = "0{0}".format(a_token.value.upper().strip("&O"))
    #     elif a_token.type == "NUMBER_BINARY":
    #         cvalue = "0b{0}".format(a_token.value.upper().strip("&B"))
    #     elif a_token.type == "RESERVED_OPERATOR_AND":
    #         cvalue = "&&"
    #     else:
    #         cvalue = a_token.value
    #     return cvalue

    # @staticmethod
    # def _translate_token_type_to_c(a_token):
    #     if a_token.type in ["BYTE", "CHAR", "CHARACTER", "STRING"]:
    #         ctype = "unsigned char"
    #     elif a_token.type in ["INTEGER", "SIGNED_DECIMAL"]:
    #         ctype = "int"
    #     elif a_token.type == "UNSIGNED_DECIMAL":
    #         ctype = "unsigned int"
    #     elif a_token.type in ["REAL", "SIGNED_REAL", "UNSIGNED_REAL"]:
    #         ctype = "float"
    #     elif a_token.type in ["BOOLEAN", "CONSTANT_TRUE", "CONSTANT_FALSE"]:
    #         ctype = "_Bool"
    #     elif a_token.type == "NUMBER_HEXADECIMAL":
    #         ctype = "unsigned short"
    #     elif a_token.type == "NUMBER_OCTAL":
    #         ctype = "unsigned short"
    #     elif a_token.type == "NUMBER_BINARY":
    #         ctype = "unsigned short"
    #     else:
    #         ctype = a_token.type
    #
    #     return ctype

    # def emit_action_2(self, a_token):
    #
    #     # if a_symbol.type in ["CHARACTER", "STRING"]:
    #     #     ctype = "unsigned char"
    #     #     cvalue = a_symbol.value.strip("'").strip('"')
    #     # elif a_symbol.type == "SIGNED_DECIMAL":
    #     #     ctype = "int"
    #     #     cvalue = a_symbol.value
    #     # elif a_symbol.type == "UNSIGNED_DECIMAL":
    #     #     ctype = "unsigned int"
    #     #     cvalue = a_symbol.value
    #     # elif a_symbol.type in ["SIGNED_REAL", "UNSIGNED_REAL"]:
    #     #     ctype = "float"
    #     #     cvalue = a_symbol.value
    #     # elif a_symbol.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
    #     #     ctype = "_Bool"
    #     #     cvalue = "true" if a_symbol.type == "CONSTANT_TRUE" else "false"
    #     # elif a_symbol.type == "NUMBER_HEXADECIMAL":
    #     #     ctype = "unsigned short"
    #     #     cvalue = "0x{0}".format(a_symbol.value.upper().strip("&H"))
    #     # elif a_symbol.type == "NUMBER_OCTAL":
    #     #     ctype = "unsigned short"
    #     #     cvalue = "0{0}".format(a_symbol.value.upper().strip("&O"))
    #     # elif a_symbol.type == "NUMBER_BINARY":
    #     #     ctype = "unsigned short"
    #     #     cvalue = "0b{0}".format(a_symbol.value.upper().strip("&B"))
    #     # else:
    #     #     cvalue = a_symbol.value
    #     #     ctype = a_symbol.type
    #
    #     ctype = self._translate_token_type_to_c(a_token)
    #     cvalue = self._translate_token_value_to_c(a_token)
    #
    #     if a_token.type in ["STRING"]:
    #         line = "const {0} {1} [ ] = \"{2}\";"
    #     elif a_token.type in ["CHARACTER"]:
    #         line = "const {0} {1} = '{2}';"
    #     else:
    #         line = "const {0} {1} = {2};"
    #
    #     self.emit_header_line(line.format(ctype, a_token.name, cvalue))

    # def emit_action_3(self, a_token):
    #     """
    #     VARIABLE_DECLARATION_PART
    #     """
    #     #
    #     # ctype = a_variable_symbol.type
    #     # if a_variable_symbol.type == "INTEGER":
    #     #     ctype = "int"
    #     # elif a_variable_symbol.type == "REAL":
    #     #     ctype = "float"
    #     # elif a_variable_symbol.type == "BYTE":
    #     #     ctype = "unsigned char"
    #     # elif a_variable_symbol.type == "BOOLEAN":
    #     #     ctype = "_Bool"
    #     # elif a_variable_symbol.type == "CHAR":
    #     #     ctype = "unsigned char"
    #     #
    #     ctype = self._translate_token_type_to_c(a_token)
    #     line = "{0} {1};"
    #     self.emit_header_line(line.format(ctype, a_token.name))

    # def emit_action_5(self):
    #     """
    #     RESERVED_STRUCTURE_END
    #     """
    #     self.emit_line("return 0;")
    #     self.emit_line("}")
    #
    # #def emit_action_6(self, a_symbol):
    # #    line = "{0} "
    # #    if a_symbol.type == "OPERATOR_ASSIGNMENT":
    # #        line = "= "
    # #    self.emit(line.format(a_symbol.value))

    # def emit_action_6(self, input_list):
    #     """
    #     ASSIGNMENT_STATEMENT
    #      emit assignment expressions
    #      C SYNTAX IS:  c = a + -b;
    #      INPUT IS   :  c := a + - b
    #     """
    #     for token in input_list:
    #         if token.type == "OPERATOR_MINUS":
    #             particle = "{0}"
    #         else:
    #             particle = "{0} "
    #         self.emit(particle.format(self._translate_token_value_to_c(token)))
    #     self.emit_line(";")

    # def emit_action_8(self, input_list):
    #     """
    #     REPEAT_STATEMENT
    #     """
    #     token = input_list.pop(0)
    #     if token.type == "RESERVED_STATEMENT_REPEAT":
    #         line = "do"
    #         self.emit_line(line)
    #         self.emit_line("{")
    #     elif token.type == "RESERVED_STATEMENT_UNTIL":
    #         line = "} while ( ! ( "
    #         self.emit(line)
    #         line = "{0} "
    #         for token in input_list:
    #             self.emit(line.format(self._translate_token_value_to_c(token)))
    #         line = "));"
    #         self.emit_line(line)
    #     else:
    #         raise KeyError

    # def emit_action_9(self, a_symbol):
    #     line = "{0} "
    #     self.emit(line.format(self._translate_token_value_to_c(a_symbol)))

    # def emit_action_10(self, a_symbol):
    #     line = "{0} "
    #     self.emit(line.format(self._translate_token_value_to_c(a_symbol)))


class CMOCEmitter(CEmitter):

    def emit_program_heading(self):
        self.emit_header_line("#include <cmoc.h>")
        self.emit_header_line("# define boolean	int")
        self.emit_header_line("# define true	1")
        self.emit_header_line("# define false	0")
