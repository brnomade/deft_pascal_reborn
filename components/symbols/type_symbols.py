"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseType


class PointerType(BaseType):

    @classmethod
    def reserved_type_pointer(cls):
        a_type = cls('POINTER', 'RESERVED_TYPE_POINTER', 'POINTER')
        return a_type

    @property
    def index(self):
        return 6

    @property
    def type_to_c(self):
        return "int"


class CustomType(BaseType):

    def do_nothing(self):
        pass

    @property
    def type_to_c(self):
        return "NOT IMPLEMENTED YET"


class BasicType(BaseType):

    @classmethod
    def reserved_type_integer(cls):
        a_type = cls('INTEGER', 'RESERVED_TYPE_INTEGER', 'INTEGER')
        a_type.index = 0
        return a_type

    @classmethod
    def reserved_type_real(cls):
        a_type = cls('REAL', 'RESERVED_TYPE_REAL', 'REAL')
        a_type.index = 1
        return a_type

    @classmethod
    def reserved_type_set(cls):
        a_type = cls('SET', 'RESERVED_TYPE_SET', 'SET')
        a_type.index = 2
        return a_type

    @classmethod
    def reserved_type_char(cls):
        a_type = cls('CHAR', 'RESERVED_TYPE_CHAR', 'CHAR')
        a_type.index = 3
        return a_type

    @classmethod
    def reserved_type_boolean(cls):
        a_type = cls('BOOLEAN', 'RESERVED_TYPE_BOOLEAN', 'BOOLEAN')
        a_type.index = 5
        return a_type

    @classmethod
    def reserved_type_text(cls):
        a_type = cls('TEXT', 'RESERVED_TYPE_TEXT', 'TEXT')
        a_type.index = 7
        return a_type

    @classmethod
    def reserved_type_array(cls):
        a_type = cls('ARRAY', 'RESERVED_TYPE_ARRAY', 'ARRAY')
        a_type.index = 8
        return a_type

    @classmethod
    def reserved_type_null(cls):
        a_type = cls('NULL', 'NULL', 'NULL')
        a_type.index = 9
        return a_type

    @property
    def type_to_c(self):
        if self.type == "RESERVED_TYPE_INTEGER":
            return "int"

        if self.type == "RESERVED_TYPE_REAL":
            return "double"

        if self.type == "RESERVED_TYPE_SET":
            return "NOT IMPLEMENTED YET"

        if self.type in ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_TEXT"]:
            return "unsigned char"

        if self.type == "RESERVED_TYPE_BOOLEAN":
            return "_Bool"

        if self.type == "RESERVED_TYPE_ARRAY":
            return "NOT IMPLEMENTED YET"

        if self.type == "CONSTANT_NIL":
            return "int"

        print("translation for BasicType '{0}' not yet implemented".format(self))
        return self.type


class StringType(BasicType):

    def __str__(self):
        return "{0}('{1}'|{2}[{5}]|{3}|{4})".format(self.category, self.name, self.type, self.value, self.references, self.dimension)

    def __repr__(self):
        return "{0}('{1}'|{2}[{5}]|{3}|{4})".format(self.category, self.name, self.type, self.value, self.references, self.dimension)

    def __init__(self, a_name, a_type=None, a_value=None, dimension=80):
        # 80 is the the default length of strings in DeftPascal
        # 255 is the maximum length of a string in DeftPascal
        super().__init__(a_name, a_type, a_value)
        self._dimension = dimension
        self.index = 4

    @classmethod
    def reserved_type_string(cls):
        return cls('STRING', 'RESERVED_TYPE_STRING', 'STRING')

    @property
    def dimension(self):
        return self._dimension

    @dimension.setter
    def dimension(self, new_dimension):
        self._dimension = new_dimension

    @property
    def type_to_c(self):
        return "unsigned char"
