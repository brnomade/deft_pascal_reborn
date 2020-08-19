"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseType


class PointerType(BaseType):

    @property
    def is_pointer(self):
        return True


class CustomType(BaseType):

    def do_nothing(self):
        pass


class BasicType(BaseType):

    @classmethod
    def reserved_type_integer(cls, a_scope=None, a_level=None):
        return cls('INTEGER', a_scope, a_level, 'RESERVED_TYPE_INTEGER', 'INTEGER')

    @classmethod
    def reserved_type_real(cls, a_scope=None, a_level=None):
        return cls('REAL', a_scope, a_level, 'RESERVED_TYPE_REAL', 'REAL')

    @classmethod
    def reserved_type_boolean(cls, a_scope=None, a_level=None):
        return cls('BOOLEAN', a_scope, a_level, 'RESERVED_TYPE_BOOLEAN', 'BOOLEAN')

    @classmethod
    def reserved_type_char(cls, a_scope=None, a_level=None):
        return cls('CHAR', a_scope, a_level, 'RESERVED_TYPE_CHAR', 'CHAR')

    @classmethod
    def reserved_type_string(cls, a_scope=None, a_level=None):
        return cls('STRING', a_scope, a_level, 'RESERVED_TYPE_STRING', 'STRING')

    @classmethod
    def reserved_type_text(cls, a_scope=None, a_level=None):
        return cls('TEXT', a_scope, a_level, 'RESERVED_TYPE_TEXT', 'TEXT')