from deft_pascal_lexer import DeftPascalLexer


class DeftPascalParser:

    def __init__(self):
        self._lexer = DeftPascalLexer()

    def compile(self, input_string):
        self._lexer.set_input(input_string)
        while True:
            deft_token = self._lexer.get_token()
            if not deft_token:
                break  # No more input
            else:
                print(deft_token)


