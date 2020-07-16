

class AbstractEmitter:
    def __init__(self, full_path=""):
        self.full_path = full_path + ".c"
        self.header = ""
        self.code = ""

    def emit(self, code):
        self.code += code

    def emit_line(self, code):
        self.code += code + '\n'

    def header_line(self, code):
        self.header += code + '\n'

    def write_file(self):
        with open(self.full_path, 'w') as outputFile:
            outputFile.write(self.header + self.code)


class CEmitter(AbstractEmitter):

    def emit_action_0(self):
        self.header_line("#include <stdio.h>")
        self.header_line("#include <stdbool.h>")
        self.header_line("int main(void){")

    def emit_action_1(self):
        self.emit_line("return 0;")
        self.emit_line("}")

    def emit_action_2(self, a_constant_symbol):
        #
        ctype = a_constant_symbol.type
        cvalue = a_constant_symbol.value
        #
        if a_constant_symbol.type in ["CHARACTER", "STRING"]:
            ctype = "unsigned char"
            cvalue = cvalue.strip("'").strip('"')
        elif a_constant_symbol.type == "NUMBER_DECIMAL":
            if "." in a_constant_symbol.value:
                ctype = "float"
            elif "-" in a_constant_symbol.type:
                ctype = "int"
            else:
                ctype = "unsigned int"
        elif a_constant_symbol.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
            ctype = "_Bool"
            cvalue = "true" if a_constant_symbol.type == "CONSTANT_TRUE" else "false"
        elif a_constant_symbol.type == "NUMBER_HEXADECIMAL":
            ctype = "unsigned short"
            cvalue = "0x{0}".format(cvalue.upper().strip("&H"))
        elif a_constant_symbol.type == "NUMBER_OCTAL":
            ctype = "unsigned short"
            cvalue = "0{0}".format(cvalue.upper().strip("&O"))
        elif a_constant_symbol.type == "NUMBER_BINARY":
            ctype = "unsigned short"
            cvalue = "0b{0}".format(cvalue.upper().strip("&B"))
        #
        if a_constant_symbol.type in ["STRING"]:
            line = "const {0} {1} [ ] = \"{2}\";"
        elif a_constant_symbol.type in ["CHARACTER"]:
            line = "const {0} {1} = '{2}';"
        else:
            line = "const {0} {1} = {2};"
        #
        self.emit_line(line.format(ctype, a_constant_symbol.name.upper(), cvalue))
