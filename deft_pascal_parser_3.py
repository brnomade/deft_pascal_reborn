from lark import Lark, UnexpectedToken, UnexpectedCharacters

import logging
logging.basicConfig(level=logging.DEBUG)


class DeftPascalParser:

    @staticmethod
    def _grammar():
        specification = """
        
        ?start: _file          
        
        // PROGRAM STRUCTURE 
        
        _file : _program        
              | module         
             
        module : IDENTIFIER    
        
       _program : program_heading _SEMICOLON _block DOT 
        
        program_heading : RESERVED_STRUCTURE_PROGRAM IDENTIFIER 
                        | RESERVED_STRUCTURE_PROGRAM IDENTIFIER _LEFT_PARENTHESES _identifier_list _RIGHT_PARENTHESES
                                
        _identifier_list : _identifier_list _COMMA IDENTIFIER
                         | IDENTIFIER
                      
        _block : label_declaration_part constant_definition_part variable_declaration_part _statement_part  
                      
        // LABEL DECLARATIONS
        
        label_declaration_part : RESERVED_DECLARATION_LABEL _label_list _SEMICOLON
                               |

        _label_list : _label_list _COMMA _label
                    | _label

        _label : DIGSEQ
          
        // CONSTANT DECLARATIONS  
                      
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
           
       // DATA TYPES
       
       _type_denoter : RESERVED_TYPE_REAL
                     | RESERVED_TYPE_BOOLEAN
                     | RESERVED_TYPE_BYTE
                     | RESERVED_TYPE_CHAR
                     | RESERVED_TYPE_INTEGER
                     | RESERVED_TYPE_STRING
                     | RESERVED_TYPE_TEXT
                     | RESERVED_TYPE_WORD
                     | RESERVED_TYPE_SET
                     |

       // VARIABLE DECLARATION
       
        variable_declaration_part : RESERVED_DECLARATION_VAR _variable_declaration_list _SEMICOLON
                                  |  
        
        _variable_declaration_list : _variable_declaration_list _SEMICOLON variable_declaration
                                   | variable_declaration

        variable_declaration : _identifier_list _COLON _type_denoter

        // STATEMENTS

        _statement_part : compound_statement
        
        compound_statement : RESERVED_STRUCTURE_BEGIN _statement_sequence RESERVED_STRUCTURE_END
                 
        _statement_sequence : _statement_sequence _SEMICOLON _statement
                           | _statement
                           
        _statement : _open_statement
                  | _closed_statement
                  
        _open_statement : _label _COLON _non_labeled_open_statement
                       | _non_labeled_open_statement
 
        _closed_statement : _label _COLON _non_labeled_closed_statement
                         | _non_labeled_closed_statement

        _non_labeled_closed_statement : assignment_statement
                                     

        _non_labeled_open_statement : |

        assignment_statement : _variable_access _OPERATOR_ASSIGNMENT _expression

        _variable_access : IDENTIFIER
        
        _expression : _constant_expression

        IDENTIFIER: /[_A-Za-z]+[A-Za-z0-9_]*/
        
        // structure
        
        RESERVED_STRUCTURE_PROGRAM : "program"i
        RESERVED_STRUCTURE_MODULE : "module"i
        RESERVED_STRUCTURE_BEGIN : "begin"i
        RESERVED_STRUCTURE_END : "end"i
                      
        // declarations
        
        RESERVED_DECLARATION_CONST : "const"i
        RESERVED_DECLARATION_VAR : "var"i
        RESERVED_DECLARATION_LABEL : "label"i
        RESERVED_DECLARATION_TYPE : "type"i
        RESERVED_DECLARATION_PROCEDURE : "procedure"i
        RESERVED_DECLARATION_FUNCTION : "function"i

        // constants
        
        CONSTANT_TRUE : "True"
        CONSTANT_FALSE : "False"
        
        //types
        
        RESERVED_TYPE_ARRAY : "array"i
        RESERVED_TYPE_BOOLEAN : "boolean"i
        RESERVED_TYPE_BYTE : "byte"i
        RESERVED_TYPE_CHAR : "char"i
        RESERVED_TYPE_INTEGER : "integer"i
        RESERVED_TYPE_REAL : "real"i
        RESERVED_TYPE_STRING : "string"i
        RESERVED_TYPE_TEXT : "text"i
        RESERVED_TYPE_WORD : "word"i
        RESERVED_TYPE_SET : "set"i
            
        // logical operators 
        
        _OPERATOR_EQUAL_TO : "="
        _OPERATOR_NOT_EQUAL_TO : "<>"
        _OPERATOR_GREATER_OR_EQUAL_TO : ">="
        _OPERATOR_GREATER_THEN : ">"
        _OPERATOR_LESS_OR_EQUAL_TO : "<="
        _OPERATOR_LESS_THEN : "<"
        _OPERATOR_ASSIGNMENT : ":="
        
        // arithmetic operators
        
        OPERATOR_MULTIPLY : "*"
        OPERATOR_PLUS : "+"
        OPERATOR_MINUS : "-"
        OPERATOR_DIVIDE : "/"

             
        CHARACTER : /\'[\ A-Za-z0-9!\"#$%^&\'()*+,\-.\/:;<=>?@\[\]]\'/
        STRING : /\'[\ A-Za-z0-9!\"#$%^&()*+,\-.\/:;<=>?@\[\]]{2,}\'/
        NUMBER_DECIMAL : /[+-]?\d+([.]\d+(E[+-]?\d+)?)?/
        NUMBER_HEXADECIMAL : /\&[Hh][0-9A-F]+|\$[0-9A-F]+/
        NUMBER_OCTAL : /\&[Oo][0-7]+/
        NUMBER_BINARY : /\&[Bb][0-1]+/
        DIGSEQ : /\d+/
        
        _SEMICOLON : ";"
        DOT : "."
        _LEFT_PARENTHESES : "("
        _RIGHT_PARENTHESES : ")"
        _COMMA : ","
        _COLON : ":"
        
       
        %ignore /[\t \f\\n]+/  
        """
        return specification

    def __init__(self):
        parser = Lark(self._grammar(), parser='lalr', debug=True)
        self._parser = parser.parse

    def parse(self, a_program):
        return self._parser(a_program)


