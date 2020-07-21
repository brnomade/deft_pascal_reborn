

class AbstractEmitter:
    def __init__(self, full_path=""):
        self.full_path = full_path + ".c"
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

    def emit_action_0(self):
        self.emit_header_line("#include <stdio.h>")
        self.emit_header_line("#include <stdbool.h>")

    def emit_action_1(self):
        self.emit_line("int main(void){")

    def emit_action_2(self, a_symbol):

        if a_symbol.type in ["CHARACTER", "STRING"]:
            ctype = "unsigned char"
            cvalue = a_symbol.value.strip("'").strip('"')
        elif a_symbol.type == "SIGNED_DECIMAL":
            ctype = "int"
            cvalue = a_symbol.value
        elif a_symbol.type == "UNSIGNED_DECIMAL":
            ctype = "unsigned int"
            cvalue = a_symbol.value
        elif a_symbol.type in ["SIGNED_REAL", "UNSIGNED_REAL"]:
            ctype = "float"
            cvalue = a_symbol.value
        elif a_symbol.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
            ctype = "_Bool"
            cvalue = "true" if a_symbol.type == "CONSTANT_TRUE" else "false"
        elif a_symbol.type == "NUMBER_HEXADECIMAL":
            ctype = "unsigned short"
            cvalue = "0x{0}".format(a_symbol.value.upper().strip("&H"))
        elif a_symbol.type == "NUMBER_OCTAL":
            ctype = "unsigned short"
            cvalue = "0{0}".format(a_symbol.value.upper().strip("&O"))
        elif a_symbol.type == "NUMBER_BINARY":
            ctype = "unsigned short"
            cvalue = "0b{0}".format(a_symbol.value.upper().strip("&B"))
        else:
            cvalue = a_symbol.value
            ctype = a_symbol.type

        if a_symbol.type in ["STRING"]:
            line = "const {0} {1} [ ] = \"{2}\";"
        elif a_symbol.type in ["CHARACTER"]:
            line = "const {0} {1} = '{2}';"
        else:
            line = "const {0} {1} = {2};"

        self.emit_header_line(line.format(ctype, a_symbol.name, cvalue))


    def emit_action_3(self, a_variable_symbol):
        #
        ctype = a_variable_symbol.type
        if a_variable_symbol.type == "INTEGER":
            ctype = "int"
        elif a_variable_symbol.type == "REAL":
            ctype = "float"
        elif a_variable_symbol.type == "BYTE":
            ctype = "unsigned char"
        elif a_variable_symbol.type == "BOOLEAN":
            ctype = "_Bool"
        elif a_variable_symbol.type == "CHAR":
            ctype = "unsigned char"
        #
        line = "{0} {1};"
        self.emit_header_line(line.format(ctype, a_variable_symbol.name))

    def emit_action_5(self):
        self.emit_line("return 0;")
        self.emit_line("}")

    def emit_action_6(self, a_symbol):
        line = "{0} "
        if a_symbol.type == "OPERATOR_ASSIGNMENT":
            line = "= "
        self.emit(line.format(a_symbol.value))

    def emit_action_6_finish(self):
        line = ";"
        self.emit_line(line)

    def emit_action_8(self, step):
        if step == 1:
            line = "do"
            self.emit_line(line)
            self.emit_line("{")
        elif step == 2:
            line = "} while (!("
            self.emit(line)
        elif step == 3:
            line = "));"
            self.emit_line(line)
        else:
            raise KeyError

    def emit_action_9(self, a_symbol):
        line = "{0} "
        self.emit(line.format(a_symbol.value))

    def emit_action_10(self, a_symbol):
        line = "{0} "
        self.emit(line.format(a_symbol.value))
