"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

import os
import logging


class AbstractEmitter:
    def __init__(self, file_name, dir_path="output\\sources"):
        path = os.getcwd()
        self.full_path = os.path.join(path, dir_path, file_name + ".c")

    @property
    def output_code(self):
        raise NotImplementedError("Must be implemented by subclass.")

    def write_file(self):
        with open(self.full_path, 'w') as outputFile:
            outputFile.write(self.output_code)


class NodeBasedEmitter(AbstractEmitter):
    """
        anatomy of C program:

        HEADER SECTION
            #include <stdio.h>
            #include <stdbool.h>
            #include <string.h>

        DECLARATION SECTION ((VARIABLE, CONSTANT and FUNCTIONS)
            const char C1 ;
            const char C2[81] ;
            const char C5 ;
            const char C6[81] ;
            int sum(int I1, int I2);

        FUNCTIONS DECLARATION SECTION

            f1 -> always the main
            f2 -> any other function defined
            f3 -> any other function defined

        FUNCTION DEFINITION SECTION (FOR EACH FUNCTION)

            HEADER SECTION
               int main() {

            DECLARATION SECTION (VARIABLE, CONSTANT)
                const char C1 = 'C' ;
                const char C2[81] = "C8C8C8C8";
                C5 = C1;
                strcpy(c6, c2);

            LOCAL DEFINITION SECTION (VARIABLE, CONSTANT)

            BODY
                printf("%c\t\n", C1 ); ;
                printf("%c\t\n", C5 ); ;
                printf("%s\t\n", C2 ); ;
                printf("%s\t\n", C6 ); ;

            CLOSURE
                return 0;
                 }

            HEADER SECTION
                int max(int num1, int num2) {

            VARIABLE & CONSTANT DECLARATION SECTION
                /* local variable declaration */
                int result;

            BODY
               if (num1 > num2)
                  result = num1;
               else
                  result = num2;

            CLOSURE
                   return result;
                }

    """

    logging.basicConfig()
    _GLB_LOGGER = logging.getLogger("TreeBasedEmitter")

    def __init__(self, file_name, dir_path="output\\sources"):
        super().__init__(file_name, dir_path)
        self._source = dict()
        self._source["root"] = self.new_node()
        self._source["main"] = self.new_node()

    @classmethod
    def new_node(cls):
        return {"header": "",
                "declaration: "","
                "f_declaration" : "",
                "definition": "",
                "body": "",
                "closure": ""
                }

    def _serialise(self, node_name, input_list):
        result = ""
        for i in input_list:
            result += self[node_name][i]
        return result

    def output_code(self):
        result = self._serialise("root", ["header", "declaration", "f_declaration"])
        result += self._serialise("main", ["header", "declaration", "definition", "body", "closure"])
        for i in self._source:
            if i not in ["root", "main"]:
                result += self._serialise(i, ["header", "declaration", "f_declaration", "definition", "body", "closure"])
        return result

    def _emit(self, scope, context, input_source, line_break=False, terminator=False):
        suffix_particle = ''
        if line_break:
            suffix_particle = '\n'

        terminator_particle = ''
        if terminator:
            terminator_particle = ";"

        self._source[scope][context] += input_source + suffix_particle + terminator_particle

    def emit_header(self, scope, input_source, line_break=False, terminator=False):
        self._emit(scope, "header", input_source, line_break)

    def emit_declaration(self, scope, input_source, line_break=False, terminator=False):
        self._emit(scope, "declaration", input_source, line_break)

    def emit_function_declaration(self, scope, input_source, line_break=False, terminator=False):
        self._emit(scope, "f_declaration", input_source, line_break)

    def emit_definition(self, scope, input_source, line_break=False, terminator=False):
        self._emit(scope, "definition", input_source, line_break)

    def emit_body(self, scope, input_source, line_break=False, terminator=False):
        self._emit(scope, "body", input_source, line_break)

    def emit_closure(self, scope, input_source, line_break=False, terminator=False):
        self._emit(scope, "closure", input_source, line_break)


class CEmitter2(NodeBasedEmitter):

    def emit_program_heading(self):
        """
        PROGRAM_HEADING
        """
        self.emit_header("root", "#include <stdio.h>", line_break=True)
        self.emit_header("root", "#include <stdbool.h>", line_break=True)
        self.emit_header("root", "#include <string.h>", line_break=True)

    def emit_constant_definition_part_string(self, in_name, in_type, dimension, in_value):
        """
        CONSTANT_DEFINITION_PART
        const type variable = expression;
        """
        line_1 = "const {0} {1}[{2}];"
        line_2 = "const {0} {1}[{2}] = {3};"

        self.emit_declaration("root",
                              line_1.format(in_type, in_name, dimension + 1),
                              line_break=True,
                              terminator=True)

        self.emit_definition("root",
                             line_2.format(in_type, in_name, dimension + 1, in_value),
                             line_break=True,
                             terminator=True)

    def emit_constant_definition_part_char(self, in_name, in_type):
        """
        CONSTANT_DEFINITION_PART
        const type variable = expression;
        """
        line_1 = "const {0} {1}"
        line_2 = "const {0} {1} = "
        self.emit_declaration("root",
                              line_1.format(in_type, in_name),
                              line_break=True,
                              terminator=True)

        self.emit_definition("root",
                             line_2.format(in_type, in_name),
                             line_break=True,
                             terminator=True)

    def emit_operator_in_definition(self, a_generic_string):
        """
        Just emits a single input string
        """
        particle = "{0} "
        self.emit_definition("root",
                             particle.format(a_generic_string),
                             line_break=False,
                             terminator=False)


class LinearEmitter(AbstractEmitter):

    logging.basicConfig()
    _GLB_LOGGER = logging.getLogger("LinearEmitter")

    def __init__(self, file_name, dir_path="output\\sources"):
        super().__init__(file_name, dir_path)
        self._header = ""
        self._code = ""

    def emit(self, input_source):
        self._code += input_source

    def emit_line(self, input_source):
        self._code += input_source + '\n'

    def emit_header(self, input_source):
        # self.header += input_source
        self._code += input_source

    def emit_header_line(self, input_source):
        # self.header += input_source + '\n'
        self._code += input_source + '\n'

    @property
    def output_code(self):
        return self._header + self._code


class CEmitter(LinearEmitter):

    def emit_singleton(self, a_generic_string):
        """
        Just emits a single input string
        """
        particle = "{0} "
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
        self.emit_header_line("#include <string.h>")

    def emit_type_definition(self):
        line = "typedef "
        self.emit_header(line)

    def emit_constant_definition_part_string(self, in_name, in_type, dimension, in_value):
        """
        CONSTANT_DEFINITION_PART
        const type variable = expression;
        """
        line = "const {0} {1}[{2}] = {3}"
        self.emit_header(line.format(in_type, in_name, dimension + 1, in_value))

    def emit_constant_definition_part_char(self, in_name, in_type):
        """
        CONSTANT_DEFINITION_PART
        const type variable = expression;
        """
        line = "const {0} {1} = "
        self.emit_header(line.format(in_type, in_name))

    def emit_constant_definition_part_pointer(self, in_name, in_type):
        """
        CONSTANT_DEFINITION_PART
        const type variable = expression;
        """
        line = "const {0} *{1} = "
        self.emit_header(line.format(in_type, in_name))

    def emit_constant_definition_part_generic_left_side(self, in_name):
        """
        CONSTANT_DEFINITION_PART
        const type variable = expression;
        #define variable (expression)
        """
        # line = "const {0} {1} = "
        # self.emit_header(line.format(in_type, in_name))
        line = "#define {0} ("
        self.emit_header(line.format(in_name))

    def emit_constant_definition_part_generic_right_side(self):
        """
        CONSTANT_DEFINITION_PART
        const type variable = expression;
        #define variable (expression)
        """
        line = ")"
        self.emit_header_line(line)


    def emit_variable_declaration_part_string(self, in_type, in_name, in_dimension):
        """
        VARIABLE_DECLARATION_PART
        """
        line = "{0} {1}[{2}];"
        self.emit_header_line(line.format(in_type, in_name, str(in_dimension)))

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

    def emit_assignment_scenario_unary_string_literal(self, in_type, in_name, in_dimension, in_value):
        particle = '{0} {1}[{2}] = "{3}"'
        self.emit(particle.format(in_type, in_name, str(in_dimension), in_value))
        self.emit_statement_terminator()

    def emit_assignment_scenario_unary_string_identifier(self, in_left, in_right):
        particle = "strcpy({0}, {1})"
        self.emit(particle.format(in_left, in_right))
        self.emit_statement_terminator()

    def emit_assignment_scenario_multiple_string_literals(self, in_left, in_right):
        particle = 'strcpy({0}, "{1}")'
        self.emit(particle.format(in_left, in_right))
        self.emit_statement_terminator()

    def emit_assignment_string_left_side(self, in_variable):
        particle = "strcpy({0},"
        self.emit(particle.format(in_variable))

    def emit_assignment_string_right_side(self):
        particle = ");"
        self.emit_line(particle)

    def emit_assignment_pointer_left_side(self, in_variable):
        particle = "*{0} "
        self.emit(particle.format(in_variable))

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
        particle = ");"
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
