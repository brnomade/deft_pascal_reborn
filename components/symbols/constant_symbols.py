"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseSymbol


class Constant(BaseSymbol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._map_to_base_type(self.type)

    @staticmethod
    def _map_to_base_type(a_type_name):
        """
        this maps the constant token names received from the parser to pascal language types
        it is needed so for the type checking process
        """
        if a_type_name in ["BOOLEAN", "CONSTANT_TRUE", "CONSTANT_FALSE"]:
            return "RESERVED_TYPE_BOOLEAN"
        elif a_type_name in ["INTEGER", "UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL", "NUMBER_HEXADECIMAL"]:
            return "RESERVED_TYPE_INTEGER"
        elif a_type_name in ["REAL", "UNSIGNED_REAL", "SIGNED_REAL"]:
            return "RESERVED_TYPE_REAL"
        elif a_type_name in ["CHAR", "CHARACTER"]:
            return "RESERVED_TYPE_CHAR"
        elif a_type_name in ["STRING_VALUE"]:
            return "RESERVED_TYPE_STRING"
        elif a_type_name in ["CONSTANT_NIL"]:
            return "RESERVED_TYPE_POINTER"
        else:
            return a_type_name


class BooleanConstant(Constant):

    @classmethod
    def true(cls, a_scope=None, a_level=None):
        return cls('CONSTANT_TRUE', a_scope, a_level, 'RESERVED_TYPE_BOOLEAN', True)

    @classmethod
    def false(cls, a_scope=None, a_level=None):
        return cls('CONSTANT_FALSE', a_scope, a_level, 'RESERVED_TYPE_BOOLEAN', False)

    @classmethod
    def from_value(cls, value, a_scope=None, a_level=None):
        return cls.true(a_scope, a_level) if str(value).upper() == 'TRUE' else cls.false(a_scope, a_level)


class NilConstant(Constant):

    @classmethod
    def nil(cls, a_scope=None, a_level=None):
        return cls('NIL', a_scope, a_level, 'RESERVED_TYPE_POINTER', 'RESERVED_TYPE_POINTER')