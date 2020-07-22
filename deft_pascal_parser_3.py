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
        
       _program : program_heading _SEMICOLON _block _DOT 
        
        program_heading : RESERVED_STRUCTURE_PROGRAM IDENTIFIER 
                        | RESERVED_STRUCTURE_PROGRAM IDENTIFIER LEFT_PARENTHESES _identifier_list RIGHT_PARENTHESES
                                
        _identifier_list : _identifier_list _COMMA IDENTIFIER
                         | IDENTIFIER
                      
        _block : label_declaration_part constant_definition_part variable_declaration_part _statement_part  
                      
        // LABEL DECLARATIONS
        
        label_declaration_part : RESERVED_DECLARATION_LABEL _label_list _SEMICOLON
                               |

        _label_list : _label_list _COMMA _label
                    | _label

        _label : UNSIGNED_DECIMAL
          
        // CONSTANT DECLARATIONS  
                      
        constant_definition_part : RESERVED_DECLARATION_CONST _constant_list
                                   |
              
        _constant_list : constant_definition 
                       | constant_definition _constant_list
                  
        constant_definition : IDENTIFIER OPERATOR_EQUAL_TO _constant_expression _SEMICOLON
        
        _constant_expression : UNSIGNED_DECIMAL
                             | SIGNED_DECIMAL
                             | UNSIGNED_REAL
                             | SIGNED_REAL
                             | NUMBER_BINARY
                             | NUMBER_OCTAL
                             | NUMBER_HEXADECIMAL
                             | CHARACTER
                             | STRING
                             | CONSTANT_TRUE
                             | CONSTANT_FALSE
                             | CONSTANT_NIL
           

       // VARIABLE DECLARATION
       
        variable_declaration_part : RESERVED_DECLARATION_VAR _variable_declaration_list _SEMICOLON
                                  |  
        
        _variable_declaration_list : _variable_declaration_list _SEMICOLON variable_declaration
                                   | variable_declaration

        variable_declaration : _identifier_list _COLON _type_denoter

        // TYPE - IN BUILT TYPE DECLARATIONS

       _type_denoter : RESERVED_TYPE_REAL
                     | RESERVED_TYPE_BOOLEAN
                     | RESERVED_TYPE_BYTE
                     | RESERVED_TYPE_CHAR
                     | RESERVED_TYPE_INTEGER
                     | RESERVED_TYPE_STRING
                     | RESERVED_TYPE_TEXT
                     | RESERVED_TYPE_WORD
                     | RESERVED_TYPE_SET
                     | _new_type

        _new_type : _new_pointer_type

        // TYPE - POINTER DECLARATION

        _new_pointer_type : UPARROW _domain_type
        UPARROW : "^"
        _domain_type : IDENTIFIER 

        // STATEMENTS

        _statement_part : _compound_statement
        
        _compound_statement : RESERVED_STRUCTURE_BEGIN _statement_sequence RESERVED_STRUCTURE_END
                 
        _statement_sequence : _statement_sequence _SEMICOLON _statement
                           | _statement
                           
        _statement : _open_statement
                  | _closed_statement
                  
        _open_statement : _label _COLON _non_labeled_open_statement
                        | _non_labeled_open_statement
 
        _closed_statement : _label _COLON _non_labeled_closed_statement
                          | _non_labeled_closed_statement

        _non_labeled_closed_statement : assignment_statement
                                      | repeat_statement
                                      | closed_for_statement
                                      | _compound_statement
                                     
        // REPEAT UNTIL                             
                                     
        repeat_statement : RESERVED_STATEMENT_REPEAT _statement_sequence RESERVED_STATEMENT_UNTIL boolean_expression

        // FOR
        
        open_for_statement : RESERVED_STATEMENT_FOR _control_variable OPERATOR_ASSIGNMENT _initial_value _direction _final_value RESERVED_STATEMENT_DO _open_statement

        closed_for_statement : RESERVED_STATEMENT_FOR _control_variable OPERATOR_ASSIGNMENT _initial_value _direction _final_value RESERVED_STATEMENT_DO _closed_statement
        
        _control_variable : IDENTIFIER
        
        _initial_value : expression
        
        _direction : RESERVED_STATEMENT_TO
                   | RESERVED_STATEMENT_DOWNTO

        _final_value : expression



        //

        _non_labeled_open_statement : |

        // ASSIGNMENT STATEMENT

        assignment_statement : _variable_access OPERATOR_ASSIGNMENT expression

        _variable_access : IDENTIFIER
         
        boolean_expression : expression 

        expression : _simple_expression
                    | _simple_expression _relop _simple_expression
 
        _simple_expression : _term
                           | _simple_expression _addop _term

        _relop : OPERATOR_EQUAL_TO
               | OPERATOR_NOT_EQUAL_TO
               | OPERATOR_LESS_THEN
               | OPERATOR_GREATER_THEN
               | OPERATOR_LESS_OR_EQUAL_TO
               | OPERATOR_GREATER_OR_EQUAL_TO
               | RESERVED_IN          
 
        _addop : OPERATOR_PLUS
               | OPERATOR_MINUS
               | RESERVED_OPERATOR_OR

        _term : _factor
              | _term _mulop _factor
              
        _mulop : OPERATOR_MULTIPLY
               | OPERATOR_DIVIDE
               | RESERVED_OPERATOR_DIV
               | RESERVED_OPERATOR_MOD
               | RESERVED_OPERATOR_AND
    
        _factor : _sign _factor
                | _exponentiation
 
        _sign : OPERATOR_PLUS
              | OPERATOR_MINUS

        _exponentiation : _primary
                        | _primary OPERATOR_STARSTAR _exponentiation
 
        _primary : _variable_access
                 | _unsigned_constant
                 | LEFT_PARENTHESES expression RIGHT_PARENTHESES
                 | RESERVED_OPERATOR_NOT _primary

        _unsigned_constant : _unsigned_number
                           | CHARACTER
                           | CONSTANT_NIL
                           | CONSTANT_TRUE
                           | CONSTANT_FALSE
                           | STRING
                           
        _unsigned_number : _unsigned_integer | _unsigned_real

        _unsigned_integer : UNSIGNED_DECIMAL
                          | NUMBER_HEXADECIMAL
                          | NUMBER_OCTAL
                          | NUMBER_BINARY
 
        _unsigned_real : UNSIGNED_REAL
       
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
        
        CONSTANT_TRUE : "true"i
        CONSTANT_FALSE : "false"i
        CONSTANT_NIL : "nil"i       
        
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
                        
        // keywords
        
        RESERVED_IN : "in"i
        RESERVED_STATEMENT_REPEAT : "repeat"i 
        RESERVED_STATEMENT_UNTIL : "until"i
        RESERVED_STATEMENT_FOR : "for"i
        RESERVED_STATEMENT_TO : "to"i
        RESERVED_STATEMENT_DO : "do"i
        RESERVED_STATEMENT_DOWNTO : "downto"i

        // logical operators 
        
        OPERATOR_EQUAL_TO : "="
        OPERATOR_NOT_EQUAL_TO : "<>"
        OPERATOR_GREATER_OR_EQUAL_TO : ">="
        OPERATOR_GREATER_THEN : ">"
        OPERATOR_LESS_OR_EQUAL_TO : "<="
        OPERATOR_LESS_THEN : "<"
        OPERATOR_ASSIGNMENT : ":="
        RESERVED_OPERATOR_OR : "or"i
        RESERVED_OPERATOR_AND : "and"i
        RESERVED_OPERATOR_NOT : "not"i
        
        // arithmetic operators
        
        OPERATOR_MULTIPLY : "*"
        OPERATOR_STARSTAR : "**"
        OPERATOR_PLUS : "+"
        OPERATOR_MINUS : "-"
        OPERATOR_DIVIDE : "/"
        RESERVED_OPERATOR_MOD : "mod"i
        RESERVED_OPERATOR_DIV : "div"i
        
        // regular expressions
             
        IDENTIFIER: /[_A-Za-z]+[A-Za-z0-9_]*/
        CHARACTER : /\'[\ A-Za-z0-9!\"#$%^&\'()*+,\-.\/:;<=>?@\[\]]\'/
        STRING : /\'[\ A-Za-z0-9!\"#$%^&()*+,\-.\/:;<=>?@\[\]]{2,}\'/
        SIGNED_DECIMAL : /[+-]\d+/
        UNSIGNED_DECIMAL : /\d+/
        SIGNED_REAL : /[+-]\d+[.]\d+([Ee][+-]?\d+)?/
        UNSIGNED_REAL : /\d+[.]\d+([Ee][+-]?\d+)?/
        NUMBER_HEXADECIMAL : /\&[Hh][0-9A-F]+|\$[0-9A-F]+/
        NUMBER_OCTAL : /\&[Oo][0-7]+/
        NUMBER_BINARY : /\&[Bb][0-1]+/
        //DIGSEQ : /\d+/
        
        _SEMICOLON : ";"
        _DOT : "."
        LEFT_PARENTHESES : "("
        RIGHT_PARENTHESES : ")"
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


