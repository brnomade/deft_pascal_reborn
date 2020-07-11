from lark import Lark, UnexpectedToken, UnexpectedCharacters

import logging
logging.basicConfig(level=logging.DEBUG)


class DeftPascalParser:

    @staticmethod
    def _grammar():
        specification = """
        
        ?start: file          
        
        file : program        
             | module         
             
        module : IDENTIFIER    
        
        program : program_heading SEMICOLON block DOT 
        
        program_heading : RESERVED_STRUCTURE_PROGRAM IDENTIFIER
                        | RESERVED_STRUCTURE_PROGRAM IDENTIFIER LEFT_PARENTHESES identifier_list RIGHT_PARENTHESES
                                
        identifier_list : identifier_list COMMA IDENTIFIER
                        | IDENTIFIER
            
        block : constant_definition_part statement_part
              |
        
        constant_definition_part : RESERVED_DECLARATION_CONST constant_list
                                 |
        
        constant_list : constant_list constant_definition
                      | constant_definition
                  
        constant_definition : IDENTIFIER OPERATOR_EQUAL_TO constant_expression SEMICOLON
        
        constant_expression : NUMBER_DECIMAL
                            | NUMBER_BINARY
                            | NUMBER_OCTAL
                            | NUMBER_HEXADECIMAL
                            | CHARACTER
                            | STRING
                            | CONSTANT_TRUE
                            | CONSTANT_FALSE
           
        statement_part : compound_statement
        
        compound_statement : RESERVED_STRUCTURE_BEGIN RESERVED_STRUCTURE_END
                 
        IDENTIFIER: /[_A-Za-z]+[A-Za-z0-9_]*/
        
        // structure
        RESERVED_STRUCTURE_PROGRAM : "program"i
        RESERVED_STRUCTURE_MODULE : "module"i
        RESERVED_STRUCTURE_BEGIN : "begin"i
        RESERVED_STRUCTURE_END : "end"i
           
        // declarations
        RESERVED_DECLARATION_CONST : "const"i
        
        // constants
        CONSTANT_TRUE : "True"
        CONSTANT_FALSE : "False"
        
        // logical operators
        OPERATOR_EQUAL_TO : "="
             
        CHARACTER : /\'[\ A-Za-z0-9!\"#$%^&\'()*+,\-.\/:;<=>?@\[\]]\'/
        STRING : /\'[\ A-Za-z0-9!\"#$%^&()*+,\-.\/:;<=>?@\[\]]{2,}\'/
        NUMBER_DECIMAL: /[+-]?\d+([.]\d+(E[+-]?\d+)?)?/
        NUMBER_HEXADECIMAL: /\&[Hh][0-9A-F]+|\$[0-9A-F]+/
        NUMBER_OCTAL: /\&[Oo][0-7]+/
        NUMBER_BINARY: /\&[Bb][0-1]+/
        
        SEMICOLON : ";"
        DOT : "."
        LEFT_PARENTHESES : "("
        RIGHT_PARENTHESES : ")"
        COMMA : ","
        
       
        %ignore /[\t \f\\n]+/  
        """
        return specification

    def __init__(self):
        parser = Lark(self._grammar(), parser='earley', debug=True)
        self._parser = parser.parse

    def compile(self, a_program):
        return self._parser(a_program)


def test():
    test_code = "PROGRAM my_test_program;            \n" \
                "CONST C1 = 2;                       \n" \
                "C2 = 1;                             \n" \
                "C3 = 1.0;                           \n" \
                "C4 = &HFF;                          \n" \
                "C5 = &B10;                          \n" \
                "C6 = &O12;                          \n" \
                "C7 = 'C';                           \n" \
                "C8 = 'C8C8C8C8';                    \n" \
                "C9 = True;                          \n" \
                "C10 = False;                        \n" \
                "C11 = 1;                            \n" \
                "BEGIN                               \n" \
                "END   .                             \n"
    return test_code


dp = DeftPascalParser()

try:
    tree = dp.compile(test())
except UnexpectedToken as error:
    print('ERROR 1 - {0}'.format(error))
    exit(1)
except UnexpectedCharacters as error:
    print('ERROR 2 - {0}'.format(error))
    exit(1)

print(tree.pretty())

for i in tree.children:
    print(i.data)


