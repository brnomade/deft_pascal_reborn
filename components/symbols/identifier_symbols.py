"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseIdentifier, BaseExpression, BaseType
import logging


_MODULE_LOGGER = logging.getLogger(__name__)


class Identifier(BaseIdentifier):

    def do_nothing(self):
        pass


class TypeIdentifier(BaseIdentifier):

    def __init__(self, a_name, a_type):
        if not (isinstance(a_type, BaseType) or isinstance(a_type, TypeIdentifier)):
            raise ValueError("TypeIdentifier expects an instance of BaseType or TypeIdentifier")
        super().__init__(a_name,
                         a_type if isinstance(a_type, BaseType) else a_type.type,
                         None)

    def __str__(self):
        return "{0}({1}|{2})".format(self.category, self.name, self.type)

    def __repr__(self):
        return "{0}({1}|{2})".format(self.category, self.name, self.type)


class ConstantIdentifier(BaseIdentifier):

    def __init__(self, a_name, an_expression):
        if not isinstance(an_expression, BaseExpression):
            raise ValueError("ConstantIdentifier expects an instance of BaseExpression")
        super().__init__(a_name, None, an_expression)

    @property
    def type(self):
        if self.value is None:
            return None
        else:
            return self.value.native_type

    @type.setter
    def type(self, new_type):
        raise KeyError("ConstantIdentifiers derive their type from their expression")


    def complies_to_type_restrictions(self):
        """
        (DEFT PASCAL)
        HEXADECIMAL -> 0 to FFFF -> unsigned short
        INTEGER/DECIMAL -> -32768 to 32767 -> short
        REAL -> 1E-64 to 9E+63
        CHAR -> 0 to 255 -> unsigned char
        STRING -> 80 CHARACTERS
        TEXT -> 286 BYTES

        A constant will always have an GenericExpression as its value.
        The expression can be have a single token (a list with a single token) or a list of tokens as its value.
        Example: GenericExpression('GENERIC_EXPRESSION'|GENERIC_EXPRESSION|[NumericLiteral('&B10000000000000000'|RESERVED_TYPE_INTEGER|&B10000000000000000|scenario_large_binary_number_raises_compiler_error|0|[])]|None|None|[])
        In case the expression has a single token, it is possible to evaluate the compliance.
        In case the expression is complex, it is not possible to evaluate at compilation time without resolving the expression.
        So this routine returns:
         - None if the expression is complex
         - True or False if the expression is simple
        """
        expression_is_complex = self.value.cardinality > 1
        if expression_is_complex:
            return None

        if self.value.value[0].category == "ConstantIdentifier":
            return self.value.value[0].complies_to_type_restrictions()

        valid = True
        if self.type == "RESERVED_TYPE_INTEGER":
            value_to_check = self.value.value[0].value.upper()
            if "&B" in value_to_check:     # == "NUMBER_BINARY"
                valid = 0 <= int(value_to_check.replace("&B", "0b"), 2) <= 65535
            elif "&H" in value_to_check:   # == "NUMBER_HEXADECIMAL"
                valid = 0 <= int(value_to_check.replace("&H", "0x"), 16) <= 65535
            elif "&O" in value_to_check:   # == "NUMBER_OCTAL"
                valid = 0 <= int(value_to_check.replace("&O", "0o"), 8) <= 65535
            else:
                valid = (0 <= int(value_to_check) <= 65535) or (-32768 <= int(value_to_check) <= 32767)
        elif self.type in ["RESERVED_TYPE_STRING", "STRING_VALUE"]:
            valid = self.value.value[0].length <= 80
        return valid

    def to_literal(self):
        """
        returns the literal used in a chain of constant expressions
        return None if the constant expression is complex
        """
        if self.value.value[0].category == "ConstantIdentifier":
            return self.value.value[0].to_literal()
        else:
            return self.value.value[0]


class PointerIdentifier(BaseIdentifier):

    @property
    def is_pointer(self):
        return True


class ProcedureIdentifier(BaseIdentifier):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._argument_list = []

    @classmethod
    def unlimited_arguments_counter(cls):
        return -1

    def add_argument(self, a_symbol):
        assert type(a_symbol).__name__ == "FormalParameter"
        self._argument_list.append(a_symbol)

    @property
    def arguments(self):
        return self._argument_list

    @property
    def argument_counter(self):
        return len(self._argument_list)

    def is_parameter_compatible(self, a_symbol, argument_index):
        assert type(a_symbol).__name__ == "ActualParameter"
        assert isinstance(argument_index, int)
        if argument_index > self.argument_counter or argument_index < 1:
            return None
        else:
            return a_symbol.type == self._argument_list[argument_index - 1].type

    def accepts_parameters_count(self, parameter_count):
        return self.argument_counter == parameter_count


class InBuiltProcedureWrite(ProcedureIdentifier):

    @classmethod
    def in_built_procedure_write(cls):

        # TODO: Revisit the use of type POINTER for procedures.
        # TODO: probably procedures need to be of a NULL type so that they cannot be mixed in expressions.
        # TODO: the default "type" could be initialised in the class constructor instead of passing by parameter here.

        write = cls('write', 'RESERVED_TYPE_POINTER')
        return write

    @classmethod
    def in_built_procedure_writeln(cls):
        write = cls.in_built_procedure_write()
        write.name = "writeln"
        return write

    def add_argument(self, a_symbol):
        raise AttributeError("procedure write cannot be extended with new arguments")

    @property
    def arguments(self):
        raise AttributeError("procedure write cannot be inquired about its arguments")

    @property
    def argument_counter(self):
        return self.unlimited_arguments_counter()

    def is_parameter_compatible(self, a_symbol, argument_index):
        assert type(a_symbol).__name__ == "ActualParameter"
        assert isinstance(argument_index, int)
        return a_symbol.type.type in ["RESERVED_TYPE_INTEGER","RESERVED_TYPE_REAL",
                                      "RESERVED_TYPE_SET", "RESERVED_TYPE_CHAR",
                                      "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_STRING"]

    def accepts_parameters_count(self, parameter_count):
        return True


class ProcedureForwardIdentifier(ProcedureIdentifier):

    @classmethod
    def in_built_procedure_write(cls):
        raise TypeError("in built procedure not compatible with forward procedure type")

    @classmethod
    def in_built_procedure_writeln(cls):
        raise TypeError("in built procedure not compatible with forward procedure type")


class ProcedureExternalIdentifier(ProcedureIdentifier):
    @classmethod
    def in_built_procedure_write(cls):
        raise TypeError("in built procedure not compatible with forward procedure type")

    @classmethod
    def in_built_procedure_writeln(cls):
        raise TypeError("in built procedure not compatible with forward procedure type")
