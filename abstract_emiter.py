import os


class AbstractEmitter:
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

    def write_file(self):
        with open(self.full_path, 'w') as outputFile:
            outputFile.write(self.header + self.code)


class CEmitter(AbstractEmitter):

    @staticmethod
    def _translate_token_value_to_c(a_token):
        # translates a pascal symbol to c
        if a_token.type == "OPERATOR_ASSIGNMENT":
            cvalue = "="
        elif a_token.type in ["CHARACTER", "STRING"]:
            cvalue = a_token.value.strip("'").strip('"')
        elif a_token.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
            cvalue = "true" if a_token.type == "CONSTANT_TRUE" else "false"
        elif a_token.type == "NUMBER_HEXADECIMAL":
            cvalue = "0x{0}".format(a_token.value.upper().strip("&H"))
        elif a_token.type == "NUMBER_OCTAL":
            cvalue = "0{0}".format(a_token.value.upper().strip("&O"))
        elif a_token.type == "NUMBER_BINARY":
            cvalue = "0b{0}".format(a_token.value.upper().strip("&B"))
        elif a_token.type == "RESERVED_OPERATOR_AND":
            cvalue = "&&"
        else:
            cvalue = a_token.value
        return cvalue


    @staticmethod
    def _translate_token_type_to_c(a_token):
        if a_token.type in ["BYTE", "CHAR", "CHARACTER", "STRING"]:
            ctype = "unsigned char"
        elif a_token.type in ["INTEGER", "SIGNED_DECIMAL"]:
            ctype = "int"
        elif a_token.type == "UNSIGNED_DECIMAL":
            ctype = "unsigned int"
        elif a_token.type in ["REAL", "SIGNED_REAL", "UNSIGNED_REAL"]:
            ctype = "float"
        elif a_token.type in ["BOOLEAN", "CONSTANT_TRUE", "CONSTANT_FALSE"]:
            ctype = "_Bool"
        elif a_token.type == "NUMBER_HEXADECIMAL":
            ctype = "unsigned short"
        elif a_token.type == "NUMBER_OCTAL":
            ctype = "unsigned short"
        elif a_token.type == "NUMBER_BINARY":
            ctype = "unsigned short"
        else:
            ctype = a_token.type

        return ctype

    def action_0(self):
        """
        PROGRAM_HEADING
        """
        self.emit_header_line("#include <stdio.h>")
        self.emit_header_line("#include <stdbool.h>")

    def emit_action_1(self):
        """
        RESERVED_STRUCTURE_BEGIN
        """
        self.emit_line("int main(void){")

    def emit_action_2(self, a_token):

        # if a_symbol.type in ["CHARACTER", "STRING"]:
        #     ctype = "unsigned char"
        #     cvalue = a_symbol.value.strip("'").strip('"')
        # elif a_symbol.type == "SIGNED_DECIMAL":
        #     ctype = "int"
        #     cvalue = a_symbol.value
        # elif a_symbol.type == "UNSIGNED_DECIMAL":
        #     ctype = "unsigned int"
        #     cvalue = a_symbol.value
        # elif a_symbol.type in ["SIGNED_REAL", "UNSIGNED_REAL"]:
        #     ctype = "float"
        #     cvalue = a_symbol.value
        # elif a_symbol.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
        #     ctype = "_Bool"
        #     cvalue = "true" if a_symbol.type == "CONSTANT_TRUE" else "false"
        # elif a_symbol.type == "NUMBER_HEXADECIMAL":
        #     ctype = "unsigned short"
        #     cvalue = "0x{0}".format(a_symbol.value.upper().strip("&H"))
        # elif a_symbol.type == "NUMBER_OCTAL":
        #     ctype = "unsigned short"
        #     cvalue = "0{0}".format(a_symbol.value.upper().strip("&O"))
        # elif a_symbol.type == "NUMBER_BINARY":
        #     ctype = "unsigned short"
        #     cvalue = "0b{0}".format(a_symbol.value.upper().strip("&B"))
        # else:
        #     cvalue = a_symbol.value
        #     ctype = a_symbol.type

        ctype = self._translate_token_type_to_c(a_token)
        cvalue = self._translate_token_value_to_c(a_token)

        if a_token.type in ["STRING"]:
            line = "const {0} {1} [ ] = \"{2}\";"
        elif a_token.type in ["CHARACTER"]:
            line = "const {0} {1} = '{2}';"
        else:
            line = "const {0} {1} = {2};"

        self.emit_header_line(line.format(ctype, a_token.name, cvalue))


    def emit_action_3(self, a_token):
        """
        VARIABLE_DECLARATION_PART
        """
        #
        # ctype = a_variable_symbol.type
        # if a_variable_symbol.type == "INTEGER":
        #     ctype = "int"
        # elif a_variable_symbol.type == "REAL":
        #     ctype = "float"
        # elif a_variable_symbol.type == "BYTE":
        #     ctype = "unsigned char"
        # elif a_variable_symbol.type == "BOOLEAN":
        #     ctype = "_Bool"
        # elif a_variable_symbol.type == "CHAR":
        #     ctype = "unsigned char"
        #
        ctype = self._translate_token_type_to_c(a_token)
        line = "{0} {1};"
        self.emit_header_line(line.format(ctype, a_token.name))

    def emit_action_5(self):
        """
        RESERVED_STRUCTURE_END
        """
        self.emit_line("return 0;")
        self.emit_line("}")

    #def emit_action_6(self, a_symbol):
    #    line = "{0} "
    #    if a_symbol.type == "OPERATOR_ASSIGNMENT":
    #        line = "= "
    #    self.emit(line.format(a_symbol.value))

    def emit_action_6(self, input_list):
        """
        ASSIGNMENT_STATEMENT
         emit assignment expressions
         C SYNTAX IS:  c = a + -b;
         INPUT IS   :  c := a + - b
        """
        for token in input_list:
            if token.type == "OPERATOR_MINUS":
                particle = "{0}"
            else:
                particle = "{0} "
            self.emit(particle.format(self._translate_token_value_to_c(token)))
        self.emit_line(";")

    def emit_action_8(self, input_list):
        """
        REPEAT_STATEMENT
        """
        token = input_list.pop(0)
        if token.type == "RESERVED_STATEMENT_REPEAT":
            line = "do"
            self.emit_line(line)
            self.emit_line("{")
        elif token.type == "RESERVED_STATEMENT_UNTIL":
            line = "} while ( ! ( "
            self.emit(line)
            line = "{0} "
            for token in input_list:
                self.emit(line.format(self._translate_token_value_to_c(token)))
            line = "));"
            self.emit_line(line)
        else:
            raise KeyError

    def emit_action_9(self, a_symbol):
        line = "{0} "
        self.emit(line.format(self._translate_token_value_to_c(a_symbol)))

    def emit_action_10(self, a_symbol):
        line = "{0} "
        self.emit(line.format(self._translate_token_value_to_c(a_symbol)))
