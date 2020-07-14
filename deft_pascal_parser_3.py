from lark import Lark, UnexpectedToken, UnexpectedCharacters

import logging
logging.basicConfig(level=logging.DEBUG)


class DeftPascalParser:

    @staticmethod
    def _grammar():
        specification = """
        
        ?start: _file          
        
        _file : _program        
              | module         
             
        module : IDENTIFIER    
        
        // REF pascal_program : program_header declarations compound_statement DOT
        // REF program_header : RESERVED_STRUCTURE_PROGRAM IDENTIFIER SEMICOLON
        // REF declarations : constant_definitions variable_declarations
        
        _program : program_heading _SEMICOLON _block DOT 
        
        program_heading : RESERVED_STRUCTURE_PROGRAM IDENTIFIER 
                        | RESERVED_STRUCTURE_PROGRAM IDENTIFIER _LEFT_PARENTHESES _identifier_list _RIGHT_PARENTHESES
                                
        _identifier_list : _identifier_list _COMMA IDENTIFIER
                        | IDENTIFIER
                      
        _block : constant_definition_part statement_part  
                      
        // RULES FOR CONSTANT DECLARATIONS  
                      
        constant_definition_part : RESERVED_DECLARATION_CONST _constant_list
                                   |
              
        _constant_list : constant_definition 
                       | constant_definition _constant_list
                  
        constant_definition : IDENTIFIER _OPERATOR_EQUAL_TO _constant_expression _SEMICOLON
        
        _constant_expression : NUMBER_DECIMAL
                             | NUMBER_BINARY
                             | NUMBER_OCTAL
                             | NUMBER_HEXADECIMAL
                             | CHARACTER
                             | STRING
                             | CONSTANT_TRUE
                             | CONSTANT_FALSE
           
        statement_part : compound_statement
        
        compound_statement : RESERVED_STRUCTURE_BEGIN statement_sequence RESERVED_STRUCTURE_END
                 
        statement_sequence : statement_sequence _SEMICOLON statement
                           | statement
        statement : DOT
                  |
 
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
        _OPERATOR_EQUAL_TO : "="
             
        CHARACTER : /\'[\ A-Za-z0-9!\"#$%^&\'()*+,\-.\/:;<=>?@\[\]]\'/
        STRING : /\'[\ A-Za-z0-9!\"#$%^&()*+,\-.\/:;<=>?@\[\]]{2,}\'/
        NUMBER_DECIMAL: /[+-]?\d+([.]\d+(E[+-]?\d+)?)?/
        NUMBER_HEXADECIMAL: /\&[Hh][0-9A-F]+|\$[0-9A-F]+/
        NUMBER_OCTAL: /\&[Oo][0-7]+/
        NUMBER_BINARY: /\&[Bb][0-1]+/
        
        _SEMICOLON : ";"
        DOT : "."
        _LEFT_PARENTHESES : "("
        _RIGHT_PARENTHESES : ")"
        _COMMA : ","
        
       
        %ignore /[\t \f\\n]+/  
        """
        return specification

    def __init__(self):
        parser = Lark(self._grammar(), parser='lalr', debug=True)
        self._parser = parser.parse

    def compile(self, a_program):
        return self._parser(a_program)


