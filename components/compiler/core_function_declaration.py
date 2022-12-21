"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.identifier_symbols import FunctionExternalIdentifier, FunctionForwardIdentifier, \
                                                  FunctionIdentifier


class FunctionProcessor:

    def __init__(self, ast, action_name):
        self._ast = ast
        self._action_name = action_name
        self._directive = None
        self._type_descriptor = {"is_string": False,
                                 "dimension": None,
                                 "type": None
                                }

    def assert_context_is_valid(self):
        # set the context
        context = self._ast.pop(0).upper()
        if context != "FUNCTION":
            raise ValueError("Internal Error - Unknown context '{0}' in action '{1}'".format(context,
                                                                                             self._action_name))
        return context

    def assert_directive_is_valid(self):
        if self._ast[-1].data.upper() != "DIRECTIVE":
            raise KeyError("Internal Error - Unexpected keyword '{0}' in action '{1}'".format(self._ast[-1].data,
                                                                                              self._action_name))
        else:
            self._directive = self._ast[-1].children[0].value.upper()
        if self._directive not in ["FORWARD", "EXTERNAL"]:
            raise KeyError("Internal Error - Unknown directive '{0}' in action '{1}'".format(self._ast[-1].data,
                                                                                             self._action_name))
        self._ast.pop(-1)

    def get_identifier(self):
        return self._ast.pop(0).value

    def get_return_type(self):
        # as we are dealing with a function, a type declaration is expected
        if self._ast[-1].data.upper() == "RETURN_TYPE":
            type_identifier = self._ast.pop(-1).children
        elif self._ast[-1].data.upper() == "FUNCTION_BLOCK":
            type_identifier = self._ast.pop(-2).children
        else:
            raise KeyError("Unexpected keyword '{0}' in action '{1}'".format(self._ast[-1].data,
                                                                             self._action_name))
        string_dimension = None
        if type_identifier[-1].type == "RIGHT_PARENTHESES":  # handling the string with dimension special case
            type_identifier.pop(-1)  # discard the )
            string_dimension = type_identifier.pop(-1)
            type_identifier.pop(-1)  # discard the (
            self._type_descriptor["is_string"] = True
            self._type_descriptor["dimension"] = string_dimension

        type_identifier = type_identifier[0]
        if type_identifier.type == "IDENTIFIER":
            # identifier is of a custom type and their definition is case sensitive/relevant
            type_identifier = type_identifier.value
        else:
            # identifier is a basic type and those are stored in the symbol table as uppercase
            type_identifier = type_identifier.value.upper()

        self._type_descriptor["type"] = type_identifier
        return type_identifier

    def function_returns_string(self):
        return self._type_descriptor["is_string"]

    def get_function_string_dimensions(self):
        if not self._type_descriptor["is_string"]:
            raise ValueError("Internal Error - Incorrect request from a Non-String function in action '{0}'".format(self._action_name))
        return self._type_descriptor["dimension"]

    def get_function_instance(self, identifier, type_symbol):
        if self._directive and (self._directive == "FORWARD"):
            function_class_name = FunctionForwardIdentifier
        elif self._directive and (self._directive == "EXTERNAL"):
            function_class_name = FunctionExternalIdentifier
        else:
            function_class_name = FunctionIdentifier
        return function_class_name(identifier, type_symbol, None)

    def function_has_arguments(self):
        return len(self._ast) > 0 and (self._ast[0].data.upper() == "PARAMETER_LIST")

    def get_arguments_list(self):
        argument_list = self._ast.pop(0).children
        # discard open and close parameters characters -> (  )
        argument_list.pop(0)
        argument_list.pop(-1)
        return argument_list
