"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2021- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.emiters.abstract_emiter import AbstractTemplateBasedEmiter


class CEmitter(AbstractTemplateBasedEmiter):

    _CLS_TEMPLATE_DICT = {"RESERVED_STRUCTURE_PROGRAM": {"file": "c_reserved_structure_program.txt",
                                                           "variable": ""},
                          "PROGRAM_HEADING": {"file": "c_program_header.txt",
                                              "variable": ""},
                          "INCLUDE_STATEMENT": {"file": "c_include_statements.txt",
                                                "variable": "DEFAULT_INPUT"},
                          "CONSTANT_DEFINITION_PART": {"file": "c_constant_declarations.txt",
                                                    "variable": "DEFAULT_INPUT"},
                          "VARIABLE_DECLARATION_PART": {"file": "c_variable_declarations.txt",
                                                    "variable": "DEFAULT_INPUT"},
                          "FUNCTION_DECLARATION_WITH_DIRECTIVE": {"file": "c_function_declaration_headers.txt",
                                                           "variable": "DEFAULT_INPUT"},
                          "FUNCTION_DECLARATION": {"file": "c_function_definition.txt",
                                                  "variable": "DEFAULT_INPUT"},
                          "PROCEDURE_DECLARATION_HEADERS": {"file": "c_procedure_declaration_headers.txt",
                                                            "variable": "DEFAULT_INPUT"},
                          "LINE_CONSTRUCTOR": {"file": "c_line_constructor.txt"},
                          }

    def __init__(self, target_template, output_file="TEMP", dir_path="tests\\output\\sources"):
        self._target = target_template
        super().__init__(self._template_source(), output_file, dir_path)

    def _template_source(self):
        return self._CLS_TEMPLATE_DICT[self._target]["file"]

    def source(self, value):
        return super()._set(self._CLS_TEMPLATE_DICT[self._target]["variable"], value)

    def _emit_singleton(self, a_generic_string):
        """
        Just emits a single input string
        """
        particle = "{0}"
        self.add_to_line(particle.format(a_generic_string))

    def _emit_singleton_line(self, a_generic_string):
        """
        Just emits a single input string
        """
        particle = "{0}\n"
        self.add_to_line(particle.format(a_generic_string))

    def emit_type_definition(self):
        line = "typedef"
        self.add_to_line(line)

    #def emit_constant_definition_part_string(self, in_name, in_type, dimension, in_value):
    #    """
    #    CONSTANT_DEFINITION_PART
    #    const type variable = expression;
    #    """
    #    line = "const {0} {1}[{2}] = {3}"
    #    self.add(line.format(in_type, in_name, dimension + 1, in_value))

    #def emit_constant_definition_part_char(self, in_name, in_type):
    #    """
    #    CONSTANT_DEFINITION_PART
    #    const type variable = expression;
    #    """
    #    line = "const {0} {1} = "
    #    self.emit_header(line.format(in_type, in_name))

    #def emit_constant_definition_part_pointer(self, in_name, in_type):
    #    """
    #    CONSTANT_DEFINITION_PART
    #    const type variable = expression;
    #    """
    #    line = "const {0} *{1} = "
    #    self.emit_header(line.format(in_type, in_name))

    #def emit_constant_definition_part_generic_left_side(self, in_name):
    #    """
    #    CONSTANT_DEFINITION_PART
    #    const type variable = expression;
    #    #define variable (expression)
    #    """
    #    # line = "const {0} {1} = "
    #    # self.emit_header(line.format(in_type, in_name))
    #    line = "#define {0} ("
    #    self.emit_header(line.format(in_name))

    #def emit_constant_definition_part_generic_right_side(self):
    #    """
    #    CONSTANT_DEFINITION_PART
    #    const type variable = expression;
    #    #define variable (expression)
    #    """
    #    line = ")"
    #    self.emit_header_line(line)

    #def emit_variable_declaration_part_string(self, in_type, in_name, in_dimension):
    #    """
    #    VARIABLE_DECLARATION_PART
    #    """
    #    line = "{0} {1}[{2}];"
    #    self.emit_header_line(line.format(in_type, in_name, str(in_dimension)))

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
        particle = "int main() {"
        self._emit_singleton_line(particle)

    def emit_reserved_structure_begin_block(self):
        """
        RESERVED_STRUCTURE_BEGIN_BLOCK
        """
        particle = " {"
        self._emit_singleton_line(particle)

    def emit_reserved_structure_end_program(self):
        """
        RESERVED_STRUCTURE_END_PROGRAM
        """
        particle = "return 0; \n }"
        self._emit_singleton_line(particle)

    def emit_reserved_structure_end_block(self):
        """
        RESERVED_STRUCTURE_END_BLOCK
        """
        line = "}"
        self._emit_singleton_line(line)

    def emit_statement_terminator(self):
        """
        STATEMENT_TERMINATOR
        """
        line = ";"
        self._emit_singleton_line(line)

    def emit_identifier(self, in_name):
        self._emit_singleton(in_name)

    def emit_literal(self, in_name):
        self._emit_singleton(in_name)

    def emit_operator(self, in_name):
        self._emit_singleton(in_name)

    def emit_symbol(self, in_name):
        self._emit_singleton(in_name)

    def emit_assignment_scenario_unary_string_literal(self, in_type, in_name, in_dimension, in_value):
        particle = '{0} {1}[{2}] = "{3}"'
        self._emit_singleton(particle.format(in_type, in_name, str(in_dimension), in_value))
        self.emit_statement_terminator()

    def emit_assignment_scenario_unary_string_identifier(self, in_left, in_right):
        particle = "strcpy({0}, {1})"
        self._emit_singleton(particle.format(in_left, in_right))
        self.emit_statement_terminator()

    def emit_assignment_scenario_multiple_string_literals(self, in_left, in_right):
        particle = 'strcpy({0}, "{1}")'
        self._emit_singleton(particle.format(in_left, in_right))
        self.emit_statement_terminator()

    def emit_assignment_string_left_side(self, in_variable):
        particle = "strcpy({0},"
        self._emit_singleton(particle.format(in_variable))

    def emit_assignment_string_right_side(self):
        line = ");"
        self._emit_singleton_line(line)

    def emit_assignment_pointer_left_side(self, in_variable):
        particle = "*{0} "
        self._emit_singleton(particle.format(in_variable))

    def emit_closed_for_statement_control_variable(self, in_variable, in_operator, start_expression):

        particle = "for ({0} {1} {2}"
        self._emit_singleton(particle.format(in_variable, in_operator, start_expression))

    def emit_closed_for_statement_to(self, in_variable, end_expression):

        particle = " ; {0} <= {1}"
        self._emit_singleton(particle.format(in_variable, end_expression))

    def emit_closed_for_statement_downto(self, in_variable, end_expression):

        particle = " ; {0} >= {1}"
        self._emit_singleton(particle.format(in_variable, end_expression))

    def emit_closed_for_statement_step_upward(self, in_variable):

        particle = "; {0} = {0} + 1)"
        self._emit_singleton(particle.format(in_variable))

    def emit_closed_for_statement_step_downward(self, in_variable):

        particle = "; {0} = {0} - 1)"
        self.emit(particle.format(in_variable))

    def emit_closed_while_statement(self):

        particle = "while ("
        self.emit(particle)

    def emit_closed_while_statement_do(self):

        particle = ")"
        self.emit_singleton(particle)

    def emit_function_return(self):
        """
        FUNCTION RETURN
        """
        particle = "return "
        self._emit_singleton(particle)

    def emit_procedure_call(self, in_procedure_name):
        """
         PROCEDURE_CALL
        """
        particle = "{0}("
        self._emit_singleton(particle.format(in_procedure_name))

    def emit_procedure_call_parameter_separator(self):
        line = ", "
        self._emit_singleton(line)

    # def emit_separator(self):
    #    line = ","
    #    self.emit_singleton(line)

    def emit_procedure_call_closure(self):
        """
         PROCEDURE_CALL
        """
        particle = ");"
        self._emit_singleton(particle)

    def emit_procedure_call_write(self):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        """
        particle = 'printf("'
        self._emit_singleton(particle)

    #def emit_procedure_call_write_format_close_with_new_line(self):
    #    """
    #    CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
    #    """
    #    particle = '\\n", '
    #    self._emit_singleton(particle)

    def emit_procedure_call_write_format_close(self, new_line_indicator):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        """
        if new_line_indicator:
            particle = '\\n", '
        else:
            particle = '", '
        self._emit_singleton(particle)

    def emit_procedure_call_write_single_argument(self, data_type, cardinality):
        """
        CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
        2 formatting particles
        """
        if cardinality == 3:
            particle = '%*.*{0}\\t'
        elif cardinality == 2:
            particle = '%*{0}\\t'
        else:
            particle = '%{0}\\t'

        if data_type in ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_BOOLEAN"]:
            data_type_indicator = "d"
        elif data_type == "RESERVED_TYPE_REAL":
            data_type_indicator = "f"
        elif data_type in ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_TEXT"]:
            data_type_indicator = "c"
        else:
            data_type_indicator = "s"

        self._emit_singleton(particle.format(data_type_indicator))

    # def emit_procedure_call_write_with_2_format(self, data_type, cardinality):
    #     """
    #     CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
    #     2 formatting particles
    #     """
    #     if cardinality == 3:
    #         particle = "%*.*{0}\\t"
    #     elif cardinality == 2:
    #         particle = "%*{0}\\t"
    #     else:
    #         particle = "%{0}\\t"
    #
    #     if data_type in ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_BOOLEAN"]:
    #         data_type_indicator = "d"
    #     elif data_type == "RESERVED_TYPE_REAL":
    #         data_type_indicator = "f"
    #     elif data_type in ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_TEXT"]:
    #         data_type_indicator = "c"
    #     else:
    #         data_type_indicator = "s"
    #
    #     self._emit_singleton(particle.format(data_type_indicator))
    #
    # def emit_procedure_call_write_with_1_format(self, data_type_indicator):
    #     """
    #     CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
    #     2 formatting particles
    #     """
    #     particle = "%*{0}\\t"
    #     self.emit(particle.format(data_type_indicator))
    #
    # def emit_procedure_call_write_with_no_format(self, data_type_indicator):
    #     """
    #     CUSTOM PROCEDURE_CALL FOR HANDLING WRITE AND WRITELN
    #     2 formatting particles
    #     """
    #     particle = "%{0}\\t"
    #     self.emit(particle.format(data_type_indicator))

    def emit_repeat_statement(self):
        line = "do {"
        self.emit_line(line)

    def emit_repeat_statement_until(self):
        particle = "} while (!("
        self.emit(particle)

    def emit_repeat_statement_until_closure(self):
        line = "));"
        self.emit_line(line)

    def emit_closed_if_statement(self, expression):
        particle = "if ({0})"
        self._emit_singleton(particle.format(expression))

    #def emit_closed_if_statement_then(self):
    #    particle = ")"
    #    self._emit_singleton_line(particle)

    def emit_closed_if_statement_else(self):
        particle = "else"
        self.emit_line(particle)

    def emit_procedure_declaration_left(self, procedure_name):
        particle = "void {0}("
        self.emit(particle.format(procedure_name))

    def emit_procedure_declaration_argument(self, in_type, in_name):
        particle = "{0} {1}"
        self.emit(particle.format(in_type, in_name))

    def emit_procedure_declaration_argument_separator(self):
        particle = ", "
        self.emit(particle)

    def emit_procedure_declaration_right(self):
        particle = ")"
        self.emit(particle)

    def emit_procedure_forward_declaration_left(self, procedure_name):
        particle = "void {0}("
        self.emit(particle.format(procedure_name))

    def emit_procedure_forward_declaration_right(self):
        particle = ");"
        self.emit_line(particle)

    def emit_procedure_external_declaration_left(self, procedure_name):
        particle = "extern void {0}("
        self.emit(particle.format(procedure_name))

    def emit_procedure_external_declaration_right(self):
        particle = ");"
        self.emit_line(particle)


class CMOCEmitter(CEmitter):

    def emit_program_heading(self):
        self.emit_header_line("#include <cmoc.h>")
        self.emit_header_line("# define boolean	int")
        self.emit_header_line("# define true	1")
        self.emit_header_line("# define false	0")

