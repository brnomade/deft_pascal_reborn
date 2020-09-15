"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseSymbol
from components.symbols.type_symbols import BasicType, StringType


class Literal(BaseSymbol):

    @classmethod
    def from_value(cls, a_value, a_type_name=None):
        raise NotImplementedError("Must be implemented by Literal subclasses")

    def value_to_c(self):
        raise NotImplementedError("Must be implemented by Literal subclasses")


class BooleanLiteral(Literal):

    @classmethod
    def true(cls):
        return cls('CONSTANT_TRUE', BasicType.reserved_type_boolean(), True)

    @classmethod
    def false(cls):
        return cls('CONSTANT_FALSE', BasicType.reserved_type_boolean(), False)

    @classmethod
    def from_value(cls, value, a_type_name=None):
        return cls.true() if str(value).upper() == 'TRUE' else cls.false()

    def value_to_c(self):
        return "true" if self.value else "false"


class NilLiteral(Literal):

    @classmethod
    def nil(cls):
        return cls('CONSTANT_NIL', BasicType.reserved_type_null(), None)

    @classmethod
    def from_value(cls, a_value, a_type_name=None):
        return cls.nil()

    def value_to_c(self):
        return "NULL"


class NumericLiteral(Literal):

    @classmethod
    def from_token(cls, parser_token):
        return cls.from_value(parser_token.value, parser_token.type)

    @classmethod
    def from_value(cls, a_value, a_type_name=None):
        if a_type_name in ["INTEGER", "UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL", "NUMBER_HEXADECIMAL"]:
            a_type = BasicType.reserved_type_integer()
        elif a_type_name in ["REAL", "UNSIGNED_REAL", "SIGNED_REAL"]:
            a_type = BasicType.reserved_type_real()
        else:
            raise ValueError("'{0}' is incompatible with '{1}'".format(a_type_name, "NumericLiteral"))
        return cls(str(a_value), a_type, a_value)

    def value_to_c(self):
        if self.type.type == "RESERVED_TYPE_INTEGER":
            if "&B" in self.value.upper():  # == "NUMBER_BINARY"
                return "0b{0}".format(self.value.upper().strip("&B"))

            if "&H" in self.value.upper():  # == "NUMBER_HEXADECIMAL"
                return "0x{0}".format(self.value.upper().strip("&H"))

            if "&O" in self.value.upper():  # == "NUMBER_OCTAL"
                return "0{0}".format(self.value.upper().strip("&O"))

            return self.value

        if self.type.type == "RESERVED_TYPE_REAL":
            return self.value


class StringLiteral(Literal):

    @classmethod
    def from_value(cls, a_value, a_type_name=None):
        if a_type_name in ["CHAR", "CHARACTER"]:
            a_type = BasicType.reserved_type_char()
        elif a_type_name in ["STRING_VALUE"]:
            a_type = StringType.reserved_type_string()
        else:
            raise ValueError("'{0}' is incompatible with '{1}'".format(a_type_name, "StringLiteral"))
        return cls(str(a_value), a_type, a_value)

    def value_to_c(self):
        if self.type.type == "RESERVED_TYPE_STRING":
            return '\"{0}\"'.format(self.value.strip("'").strip('"'))
        elif self.type.type == "RESERVED_TYPE_CHAR":
            return "\'{0}\'".format(self.value.strip("'").strip('"'))
        else:
            raise NotImplementedError("Unknown type for {0}".format(self))

    @property
    def length(self):
        return len(self.value)
