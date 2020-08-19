"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseIdentifier


class Identifier(BaseIdentifier):

    def do_nothing(self):
        pass


class PointerIdentifier(BaseIdentifier):

    @property
    def is_pointer(self):
        return True


class ProcedureIdentifier(BaseIdentifier):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parameter_counter = 0

    @property
    def parameter_counter(self):
        return self._parameter_counter

    @parameter_counter.setter
    def parameter_counter(self, new_counter):
        if not isinstance(new_counter, int):
            raise ValueError("parameter_counter expects an integer value")
        self._parameter_counter = new_counter

    @classmethod
    def unlimited_parameters_list_size(cls):
        return -1

    @classmethod
    def in_built_procedure_write(cls, a_scope=None, a_level=None):
        write = cls('write', a_scope, a_level, 'RESERVED_TYPE_POINTER', None)
        write.parameter_counter = cls.unlimited_parameters_list_size()
        return write

    @classmethod
    def in_built_procedure_writeln(cls, a_scope=None, a_level=None):
        write = cls.in_built_procedure_write(a_scope, a_level)
        write.name = "writeln"
        return write