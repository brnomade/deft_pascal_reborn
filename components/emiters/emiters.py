"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2021- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from jinja2 import Template, FileSystemLoader, Environment
import os


class AbstractTemplateEmiter:

    def __init__(self, file_name, dir_path="tests\\output\\sources"):
        self._template = Environment(loader=FileSystemLoader(searchpath="./components/emiters/templates")).get_template(self._template_source())
        self._inputs = dict()
        self._full_path = os.path.join(os.getcwd(), dir_path, file_name + ".c2")

    def _template_source(self):
        raise NotImplementedError("Method must be implemented by subclass.")

    def write_file(self):
        with open(self._full_path, 'w') as outputFile:
            outputFile.write(self.emit())

    def set(self, placeholder, value):
        self._inputs[placeholder] = value

    def get(self, placeholder):
        return self._inputs.get(placeholder, None)

    def emit(self):
        return self._template.render(self._inputs)


class CProgramTemplateEmiter(AbstractTemplateEmiter):

    def _template_source(self):
        return "c_program.txt"

    def set_include_statements(self, value):
        self.set("include_statements", value)

    def set_constant_declarations(self, value):
        self.set("constant_declarations", value)

    def set_variable_declarations(self, value):
        self.set("variable_declarations", value)

    def set_variables_initialisations(self, value):
        self.set("variables_initialisations", value)

    def set_procedure_declarations(self, value):
        self.set("procedure_declarations", value)

    def set_function_declaration(self, value):
        current_content = self.get("function_declaration")
        if not current_content:
            current_content = []
        current_content.append(value)
        self.set("function_declaration", current_content)

    def set_procedure_implementations(self, value):
        self.set("procedure_implementations", value)

    def set_main_code(self, value):
        self.set("main_code", value)
