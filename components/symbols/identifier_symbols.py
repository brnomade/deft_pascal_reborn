"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseIdentifier
import logging


_MODULE_LOGGER = logging.getLogger(__name__)


class Identifier(BaseIdentifier):

    def do_nothing(self):
        pass


class ConstantIdentifier(BaseIdentifier):

    def __init__(self, a_name, an_expression):
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
        self._parameter_counter = 0
        self._parameter_list = []

    @classmethod
    def name_is_reserved_for_in_built_procedure(cls, name):
        return True if name.upper() in ["WRITE", "WRITELN"] else False

    @classmethod
    def unlimited_parameters_list_size(cls):
        return -1

    @classmethod
    def in_built_procedure_write(cls):
        write = cls('write', 'RESERVED_TYPE_POINTER', None)
        write.parameter_counter = cls.unlimited_parameters_list_size()
        return write

    @classmethod
    def in_built_procedure_writeln(cls):
        write = cls.in_built_procedure_write()
        write.name = "writeln"
        return write

    @property
    def parameter_counter(self):
        return self._parameter_counter

    @parameter_counter.setter
    def parameter_counter(self, new_counter):
        if not isinstance(new_counter, int):
            raise ValueError("parameter_counter expects an integer value")
        self._parameter_counter = new_counter

    def add_parameter_expression(self, an_expression):
        if (self._parameter_counter == self.unlimited_parameters_list_size()) or (len(self._parameter_list) < self._parameter_counter):
            self._parameter_list.append(an_expression)
            return True
            #TODO - type check of the incoming expression against what is expected by the procedure parameter
        else:
            _MODULE_LOGGER.error("PrcedureIdentifier accepts only '{0}' parameters. Received '{1}'".format(self.parameter_counter, an_expression))
            return False
