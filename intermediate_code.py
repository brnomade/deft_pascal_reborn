from abstract_emiter import CEmitter
from symbols import Identifier

_stack_size = 1000


class IntermediateCode:

    def __init__(self):
        self._i_stack = [None] * _stack_size
        self._top = 0
        self._temp_stack = []

    def __str__(self):
        my_representation = "\n\n{0}(".format(type(self).__name__)
        for i in range(0, self._top):
            my_representation += "\n"
            my_representation += str(self._i_stack[i])
        my_representation += "\n)\n"
        return my_representation

    def __repr__(self):
        my_representation = "\n\n{0}(".format(type(self).__name__)
        for i in range(0, self._top):
            my_representation += "\n"
            my_representation += str(self._i_stack[i])
        my_representation += "\n)\n"
        return my_representation

    def _advance_top(self):
        self._top += 1
        self._temp_stack = []

    def init(self, action_number, action_name):
        self._i_stack[self._top] = {"action_number": action_number,
                                    "action_name": action_name,
                                    "token_list": None
                                    }

    def push(self, an_input):
        if isinstance(an_input, list):
            self._temp_stack += an_input
        else:
            self._temp_stack.append(an_input)

    def flush(self):
        self._i_stack[self._top]["token_list"] = self._temp_stack
        self._advance_top()

    def generate(self):
        emiter = None
        for i in range(0, self._top):

            node = self._i_stack[i]
            action_number = node["action_number"]
            token_list = node["token_list"]

            if action_number == 0:  # PROGRAM_HEADING

                emiter = CEmitter(token_list[1].value)
                emiter.emit_action_0()

            elif action_number == 1:    # RESERVED_STRUCTURE_BEGIN

                emiter.emit_action_1()

            elif action_number == 2:    # CONSTANT_DEFINITION_PART

                for token in token_list:

                    if isinstance(token, Identifier):
                        emiter.emit_action_2(token)

            elif action_number == 3:    # VARIABLE_DECLARATION_PART

                for token in token_list:

                    if isinstance(token, Identifier):
                        emiter.emit_action_3(token)

            elif action_number == 5:    # RESERVED_STRUCTURE_END

                emiter.emit_action_5()

            elif action_number == 6:    # ASSIGNMENT_STATEMENT

                emiter.emit_action_6(token_list)

            elif action_number == 8:    # REPEAT_STATEMENT

                emiter.emit_action_8(token_list)

        emiter.write_file()





