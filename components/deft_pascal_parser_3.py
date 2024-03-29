"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from lark import Lark, UnexpectedCharacters, UnexpectedToken
import logging

_MODULE_LOGGER_ = logging.getLogger("deft_pascal_reborn")


class DeftPascalParser:

    @staticmethod
    def _grammar():
        specification = """
        
        ?start: _file          
        
        // PROGRAM STRUCTURE 
        
        _file : _program        
              | module         
             
        module : IDENTIFIER    
        
       _program : program_heading _SEMICOLON _program_block _DOT 
        
        program_heading : RESERVED_STRUCTURE_PROGRAM IDENTIFIER 
                        | RESERVED_STRUCTURE_PROGRAM IDENTIFIER LEFT_PARENTHESES _identifier_list RIGHT_PARENTHESES
                                
        _identifier_list : _identifier_list COMMA IDENTIFIER
                         | IDENTIFIER
                      
        _program_block : _block
        
        _block : label_declaration_part constant_definition_part type_definition_part variable_declaration_part _procedure_and_function_declaration_part _statement_part
                             
        // LABEL DECLARATIONS
        
        label_declaration_part : RESERVED_DECLARATION_LABEL _label_list _SEMICOLON
                               |

        _label_list : _label_list COMMA _label
                    | _label

        _label : UNSIGNED_DECIMAL
          
        // CONSTANT DECLARATIONS  
                      
        constant_definition_part : RESERVED_DECLARATION_CONST _constant_list
                                   |
              
        _constant_list : constant_definition 
                       | constant_definition _constant_list
                  
        constant_definition : IDENTIFIER OPERATOR_EQUAL_TO constant_expression _SEMICOLON
        
        constant_expression : _constant_simple_expression
                            | _constant_simple_expression _relop _constant_simple_expression
        
        _constant_simple_expression : _constant_term
                                   | _constant_simple_expression _addop _constant_term

        _constant_term : _constant_factor
                       | _constant_term _mulop _constant_factor
              
        _constant_factor : _sign _constant_factor
                         | _constant_exponentiation
        
        _constant_exponentiation : _constant_primary
                                 | _constant_primary OPERATOR_STARSTAR _constant_exponentiation
         
        _constant_primary : constant_access
                          | _unsigned_constant
                          | LEFT_PARENTHESES constant_expression RIGHT_PARENTHESES
                          | OPERATOR_NOT _constant_primary

        constant_access : IDENTIFIER 


        //constant_expression : UNSIGNED_DECIMAL
        //                     | SIGNED_DECIMAL
        //                     | UNSIGNED_REAL
        //                     | SIGNED_REAL
        //                     | NUMBER_BINARY
        //                     | NUMBER_OCTAL
        //                     | NUMBER_HEXADECIMAL
        //                     | CHARACTER
        //                     | STRING_VALUE
        //                     | CONSTANT_TRUE
        //                     | CONSTANT_FALSE
        //                     | CONSTANT_NIL
           
        // TYPE DECLARATION
       
        type_definition_part : RESERVED_DECLARATION_TYPE _type_definition_list
                              |   
       
        _type_definition_list : _type_definition_list type_definition
                              | type_definition
                              
        type_definition : IDENTIFIER OPERATOR_EQUAL_TO _type_denoter _SEMICOLON

       // VARIABLE DECLARATION
       
        variable_declaration_part : RESERVED_DECLARATION_VAR _variable_declaration_list _SEMICOLON
                                  |  
        
        _variable_declaration_list : _variable_declaration_list _SEMICOLON variable_declaration
                                   | variable_declaration

        variable_declaration : _identifier_list _COLON _type_denoter


        // PROCEDURE AND FUNCTION DECLARATION
        
        procedure_and_function_declaration_part : proc_or_func_declaration_list _SEMICOLON
                                                |

        proc_or_func_declaration_list : proc_or_func_declaration_list _SEMICOLON proc_or_func_declaration
                                      | proc_or_func_declaration
 
        proc_or_func_declaration : procedure_declaration
                                 | function_declaration
                                 
        procedure_declaration : procedure_heading _SEMICOLON directive
                              | procedure_heading _SEMICOLON procedure_block
 
        procedure_heading : procedure_identification
                          | procedure_identification formal_parameter_list
 
        directive : RESERVED_STATEMENT_FORWARD
                  | RESERVED_STATEMENT_EXTERNAL

        formal_parameter_list : LEFT_PARENTHESES formal_parameter_section_list RIGHT_PARENTHESES
 
        formal_parameter_section_list : formal_parameter_section_list _SEMICOLON formal_parameter_section
                                      | formal_parameter_section

        formal_parameter_section : value_parameter_specification
                                 | variable_parameter_specification
                                 | procedural_parameter_specification
                                 | functional_parameter_specification

        value_parameter_specification : _identifier_list _COLON IDENTIFIER

        variable_parameter_specification : RESERVED_DECLARATION_VAR _identifier_list _COLON IDENTIFIER

        procedural_parameter_specification : procedure_heading

        functional_parameter_specification : function_heading                 
 
        procedure_identification : RESERVED_DECLARATION_PROCEDURE IDENTIFIER

        procedure_block : _block
        
        function_declaration : function_heading _SEMICOLON directive
                             | function_identification _SEMICOLON function_block
                             | function_heading _SEMICOLON function_block
        
        function_heading : RESERVED_DECLARATION_FUNCTION IDENTIFIER _COLON result_type
                         | RESERVED_DECLARATION_FUNCTION IDENTIFIER formal_parameter_list _COLON result_type
        
        result_type : IDENTIFIER

        function_identification : RESERVED_DECLARATION_FUNCTION IDENTIFIER

        function_block : _block


        // TYPE - IN BUILT TYPE DECLARATIONS

       _type_denoter : RESERVED_TYPE_REAL
                     | RESERVED_TYPE_BOOLEAN
                     | RESERVED_TYPE_CHAR
                     | RESERVED_TYPE_INTEGER
                     | RESERVED_TYPE_STRING
                     | RESERVED_TYPE_STRING LEFT_PARENTHESES UNSIGNED_DECIMAL RIGHT_PARENTHESES
                     | RESERVED_TYPE_TEXT
                     | RESERVED_TYPE_SET
                     | IDENTIFIER
                     | _new_type


        // TYPE - POINTER DECLARATION

        _new_type : _new_pointer_type
        
        _new_pointer_type : OPERATOR_UPARROW _domain_type
        
        _domain_type : RESERVED_TYPE_REAL
                     | RESERVED_TYPE_BOOLEAN
                     | RESERVED_TYPE_CHAR
                     | RESERVED_TYPE_INTEGER
                     | RESERVED_TYPE_STRING
                     | RESERVED_TYPE_STRING LEFT_PARENTHESES UNSIGNED_DECIMAL RIGHT_PARENTHESES
                     | RESERVED_TYPE_TEXT
                     | RESERVED_TYPE_SET
                     | IDENTIFIER 


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
                                      | procedure_call  
                                      | compound_statement
                                      | repeat_statement
                                      | closed_if_statement
                                      | closed_while_statement
                                      | closed_for_statement
                                      
        _non_labeled_open_statement : open_if_statement 
                                    | open_for_statement
                                    |
        

                                      
        // WHILE
        
        closed_while_statement : RESERVED_STATEMENT_WHILE _boolean_expression RESERVED_STATEMENT_DO _closed_statement
        
        // REPEAT UNTIL                             
                                     
        repeat_statement : RESERVED_STATEMENT_REPEAT _statement_sequence RESERVED_STATEMENT_UNTIL _boolean_expression

        // FOR
        
        open_for_statement : RESERVED_STATEMENT_FOR variable_access OPERATOR_ASSIGNMENT _initial_value _direction _final_value RESERVED_STATEMENT_DO _open_statement

        closed_for_statement : RESERVED_STATEMENT_FOR variable_access OPERATOR_ASSIGNMENT _initial_value _direction _final_value RESERVED_STATEMENT_DO _closed_statement
        
       // IF
       
       closed_if_statement : RESERVED_STATEMENT_IF _boolean_expression RESERVED_STATEMENT_THEN _closed_statement RESERVED_STATEMENT_ELSE _closed_statement

       open_if_statement : RESERVED_STATEMENT_IF _boolean_expression RESERVED_STATEMENT_THEN _statement
                         | RESERVED_STATEMENT_IF _boolean_expression RESERVED_STATEMENT_THEN _closed_statement RESERVED_STATEMENT_ELSE _open_statement
 
       
       // control_variable : IDENTIFIER
        
        _initial_value : expression
        
        _direction : RESERVED_STATEMENT_TO
                   | RESERVED_STATEMENT_DOWNTO

        _final_value : expression

        // PROCEDURE STATEMENT (PROCEDURE INVOCATION)
        
        procedure_call : IDENTIFIER _params
                       | IDENTIFIER

        _params : LEFT_PARENTHESES _actual_parameter_list RIGHT_PARENTHESES

        _actual_parameter_list : _actual_parameter_list COMMA _actual_parameter
                               | _actual_parameter

        _actual_parameter : unary_parameter
                          | binary_parameter
                          | ternary_parameter

        unary_parameter : expression
        
        binary_parameter : expression _COLON expression
        
        ternary_parameter : expression _COLON expression _COLON expression
        
        // ASSIGNMENT STATEMENT

        assignment_statement : variable_access OPERATOR_ASSIGNMENT expression

        variable_access : IDENTIFIER 
                        | variable_access OPERATOR_UPARROW
         
        _boolean_expression : expression 

        expression : _simple_expression
                    | _simple_expression _relop _simple_expression
 
        _simple_expression : _term
                           | _simple_expression _addop _term

        _relop : OPERATOR_EQUAL_TO
               | OPERATOR_NOT_EQUAL_TO
               | OPERATOR_LESS_THAN
               | OPERATOR_GREATER_THAN
               | OPERATOR_LESS_OR_EQUAL_TO
               | OPERATOR_GREATER_OR_EQUAL_TO
               | OPERATOR_IN          
 
        _addop : OPERATOR_PLUS
               | OPERATOR_MINUS
               | OPERATOR_OR

        _term : _factor
              | _term _mulop _factor
              
        _mulop : OPERATOR_MULTIPLY
               | OPERATOR_DIVIDE
               | OPERATOR_DIV
               | OPERATOR_MOD
               | OPERATOR_AND
    
        _factor : _sign _factor
                | _exponentiation
 
        _sign : OPERATOR_ARITHMETIC_NEUTRAL
              | OPERATOR_ARITHMETIC_NEGATION

        _exponentiation : _primary
                        | _primary OPERATOR_STARSTAR _exponentiation
 
        _primary : variable_access
                 | _unsigned_constant
                 | function_designator
                 | LEFT_PARENTHESES expression RIGHT_PARENTHESES
                 | OPERATOR_NOT _primary
                 

        _unsigned_constant : _unsigned_number
                           | CHARACTER
                           | CONSTANT_NIL
                           | CONSTANT_TRUE
                           | CONSTANT_FALSE
                           | STRING_VALUE
                           
        _unsigned_number : _unsigned_integer | _unsigned_real

        _unsigned_integer : UNSIGNED_DECIMAL
                          | NUMBER_HEXADECIMAL
                          | NUMBER_OCTAL
                          | NUMBER_BINARY
 
        _unsigned_real : UNSIGNED_REAL
       
        // functions with no params are handled by plain identifier
        
        function_designator : IDENTIFIER _params
       
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
        RESERVED_TYPE_CHAR : "char"i
        RESERVED_TYPE_INTEGER : "integer"i
        RESERVED_TYPE_REAL : "real"i
        RESERVED_TYPE_STRING : "string"i
        RESERVED_TYPE_TEXT : "text"i
        RESERVED_TYPE_SET : "set"i
                        
        // keywords
        
        RESERVED_STATEMENT_REPEAT : "repeat"i 
        RESERVED_STATEMENT_UNTIL : "until"i
        RESERVED_STATEMENT_FOR : "for"i
        RESERVED_STATEMENT_TO : "to"i
        RESERVED_STATEMENT_DOWNTO : "downto"i
        RESERVED_STATEMENT_DO : "do"i
        RESERVED_STATEMENT_WHILE : "while"i
        RESERVED_STATEMENT_BYTE : "byte"i
        RESERVED_STATEMENT_WORD : "word"i
        RESERVED_STATEMENT_IF : "if"i
        RESERVED_STATEMENT_THEN : "then"i  
        RESERVED_STATEMENT_ELSE : "else"i
        RESERVED_STATEMENT_FORWARD : "forward"i
        RESERVED_STATEMENT_EXTERNAL : "external"i

        // logical operators 
        
        OPERATOR_EQUAL_TO : "="
        OPERATOR_NOT_EQUAL_TO : "<>"
        OPERATOR_GREATER_OR_EQUAL_TO : ">="
        OPERATOR_GREATER_THAN : ">"
        OPERATOR_LESS_OR_EQUAL_TO : "<="
        OPERATOR_LESS_THAN : "<"
        OPERATOR_ASSIGNMENT : ":="
        OPERATOR_OR : "or"i
        OPERATOR_AND : "and"i
        OPERATOR_NOT : "not"i

        // set operators
        
        OPERATOR_IN : "in"i
        
        // bitwise operators
        OPERATOR_LSL : "lsl"i
        OPERATOR_LSR : "lsr"i
        OPERATOR_SHL : "shl"i
        OPERATOR_SHR : "shr"i
        OPERATOR_XOR : "xor"i
        
        // arithmetic operators

        OPERATOR_PLUS : "+"
        OPERATOR_ARITHMETIC_NEUTRAL : "+"
        OPERATOR_MINUS : "-"
        OPERATOR_ARITHMETIC_NEGATION : "-"
        OPERATOR_MULTIPLY : "*"
        OPERATOR_STARSTAR : "**"
        OPERATOR_DIVIDE : "/"
        OPERATOR_MOD : "mod"i
        OPERATOR_DIV : "div"i
        OPERATOR_ABS : "abs"i
        OPERATOR_UPARROW : "^"

        
        // regular expressions
             
        IDENTIFIER: /[_A-Za-z]+[A-Za-z0-9_]*/
        CHARACTER : /\'[\ A-Za-z0-9!\"#$%^&\'()*+,\-._\/:;<=>?@\[\]]\'/
        STRING_VALUE : /\'[\ A-Za-z0-9!\"#$%^&()*+,\-._\/:;<=>?@\[\]]{2,}\'/
        SIGNED_DECIMAL : /[+-]\d+/
        UNSIGNED_DECIMAL : /\d+/
        SIGNED_REAL : /[+-]\d+[.]\d+([Ee][+-]?\d+)?/
        UNSIGNED_REAL : /\d+[.]\d+([Ee][+-]?\d+)?/
        NUMBER_HEXADECIMAL : /\&[Hh][0-9A-F]+|\$[0-9A-F]+/
        NUMBER_OCTAL : /\&[Oo][0-7]+/
        NUMBER_BINARY : /\&[Bb][0-1]+/
        //DIGSEQ : /\d+/

        // SEPARATORS
        
        _SEMICOLON : ";"
        _DOT : "."
        LEFT_PARENTHESES : "("
        RIGHT_PARENTHESES : ")"
        COMMA : ","
        _COLON : ":"
       
        COMMENT : "{" /(.|\\n|\\r)+/ "}"    
                | "(*" /(.|\\n|\\r)+/ "*)"  
                | /[\t \f\\n]+/
                
        %ignore COMMENT      

        %ignore /[\t \f\\n]+/  
        """
        return specification

    def __init__(self):
        parser = Lark(self._grammar(), parser='lalr', debug=False)
        self._parser = parser.parse
        self._ast = None

    def parse(self, a_program):
        error_list = []
        try:
            self._ast = self._parser(a_program)
        except UnexpectedCharacters as error:
            msg = "syntax error at line {0} column {1}. unexpected character found. expected {2}".format(error.line, error.column, error.allowed)
            error_list.append(msg)
            _MODULE_LOGGER_.error(msg)
        except UnexpectedToken as error:
            msg = "syntax error at line {0} column {1}: expected {2}".format(error.line, error.column, error.expected)
            error_list.append(msg)
            _MODULE_LOGGER_.error(msg)
        return error_list

    @property
    def ast(self):
        if self._ast:
            return self._ast
        else:
            raise ValueError("AST is not yet defined")
