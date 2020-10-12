"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""
import inspect


class NegativeLanguageTests:

    @classmethod
    def available_tests(cls):
        """
        Only test cases named with a "scenario_" prefix are run as NegativeTests.
        Other test cases not following such pattern are used in other test classes.
        """
        return [i for i in inspect.getmembers(cls, predicate=inspect.isfunction) if 'scenario_' in i[0]]

    @staticmethod
    def syntax_error_raises_parser_error_unexpected_token():
        # triggered by test_deft_pascal_parser.py
        code = """
            PROGRAM {{{0}}}        
            BEGIN                               
            END.                                
        """
        return code

    @staticmethod
    def syntax_error_raises_parser_error_unexpected_characters():
        # triggered by test_deft_pascal_parser.py
        code = """ "
            PROGRAM {{{0}}}        
            BEGIN                               
            END.                                
        """
        return code

    @staticmethod
    def scenario_unresolved_forward_procedure_declaration_raises_error():
        code = ("unresolved forward reference", "", """
            PROGRAM {{{0}}};                   
                PROCEDURE outer_procedure; forward;
            BEGIN             
                writeln('main program');
            END.                                         
        """)
        return code


    @staticmethod
    def scenario_nested_procedure_declaration_raises_warning():
        code = ("", "nested procedure or function definition is currently not supported", """
            PROGRAM {{{0}}};                   
                PROCEDURE outer_procedure;
                    PROCEDURE inner_procedure;
                    BEGIN
                        writeln('inner_procedure');
                    END;
                BEGIN
                    writeln('outer_procedure');
                END;
            BEGIN             
                writeln('main program');
            END.                                         
        """)
        return code

    @staticmethod
    def scenario_undeclared_type_in_procedure_parameter_declaration_raises_error():
        code = ("unknown type", "", """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure(p1: UNDECLARED_TYPE); forward;
            BEGIN             
            END.                                         
        """)
        return code

    @staticmethod
    def scenario_incorrect_parameter_numbers_in_procedure_call_raises_error():
        code = ("unknown type", "", """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure(p1: integer);
                BEGIN
                    writeln('first_procedure');
                END;
            BEGIN     
              first_procedure(1,2,3);          
            END.                                         
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_basic_type_case():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : INTEGER;
            BEGIN
                V1 := True;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_case():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
            BEGIN
                V1 := True;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_dereferencing_at_left():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
            BEGIN
                V1^ := True;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_dereferencing_at_right():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
                V2 : BOOLEAN;
            BEGIN
                V2 := V1^;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_at_both_sides_derefencing():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
                V2 : ^BOOLEAN;
            BEGIN
                V1^ := V2^;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_at_both_sides():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
                V2 : ^BOOLEAN;
            BEGIN
                V1 := V2;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_at_both_sides_derefencing_right():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
                V2 : ^BOOLEAN;
            BEGIN
                V1 := V2^;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_at_both_sides_derefencing_left():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
                V2 : ^BOOLEAN;
            BEGIN
                V1^ := V2;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_compatible_pointer_types_assignment_raises_compiler_error_derefencing_right():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
                V2 : ^INTEGER;
            BEGIN
                V1 := V2^;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_compatible_pointer_types_assignment_raises_compiler_error_derefencing_left():
        code = ("incompatible types in expression", "", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
                V2 : ^INTEGER;
            BEGIN
                V1^ := V2;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_constant_identifier_already_declared_raises_compiler_error():
        code = ("already declared", "", """
            PROGRAM {{{0}}};        
            CONST 
            C1 = 'A';
            C1 = 1.0;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_assignment_to_constant_raises_compiler_error():
        code = ("invalid assignment to constant", "", """
            PROGRAM {{{0}}};
            CONST
            C1 = True;
            BEGIN
            C1 := False;
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_string_based_constant_expression_raises_compiler_error_scenario_char_literals():
        code = ("not supported", "", """
            PROGRAM {{{0}}};                
            CONST                                   
            C3 = 'C' + 'B';                                
            BEGIN                                   
            END.                                  
        """)
        return code

    @staticmethod
    def scenario_string_based_constant_expression_raises_compiler_error_scenario_strings_literals():
        code = ("not supported", "", """
            PROGRAM {{{0}}};                
            CONST                                   
            C4 = 'C8C8C8C8' + 'C8C8C8C8';                         
            BEGIN                                   
            END.                                  
        """)
        return code

    @staticmethod
    def scenario_string_based_constant_expression_raises_compiler_error_scenario_string_constants():
        code = ("not supported", "", """
            PROGRAM {{{0}}};                
            CONST                                   
            C1 = 'C';                                
            C2 = 'BBBBBBBB';                                
            C3 = C1 + C2;                                
            BEGIN                                   
            END.                                  
        """)
        return code

    @staticmethod
    def scenario_string_based_constant_expression_raises_compiler_error_scenario_string_constants_reversed_order():
        code = ("not supported", "", """
            PROGRAM {{{0}}};                
            CONST                                   
            C1 = 'C';                                
            C2 = 'BBBBBBBB';                                
            C3 = C2 + C1;                                
            BEGIN                                   
            END.                                  
        """)
        return code

    @staticmethod
    def scenario_variable_identifier_already_declared_raises_compiler_error():
        code = ("already declared", "", """
            PROGRAM {{{0}}};        
            VAR 
            V1 : INTEGER;
            V1 : REAL;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_assignment_to_undeclared_variable_identifier_raises_compiler_error():
        code = ("Reference to undeclared", "", """
            PROGRAM {{{0}}};        
            BEGIN
            V1 := True
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_variable_identifier_declared_with_undeclared_type_raises_compiler_error():
        code = ("unknown type", "", """
            PROGRAM {{{0}}};        
            VAR
            V1 : AN_UNDECLARED_TYPE;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_reference_to_undeclared_variable_identifier_raises_compiler_error():
        code = ("Reference to undeclared", "", """
            PROGRAM {{{0}}};
            VAR
            V1 : INTEGER;        
            BEGIN
            V1 := V2;
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_not_boolean_repeat_until_condition_raises_compiler_error():
        code = ("expected boolean expression", "", """
            PROGRAM {{{0}}};
            BEGIN
            REPEAT
            UNTIL 1;
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_not_boolean_while_do_condition_raises_compiler_error():
        code = ("expected boolean expression", "", """
            PROGRAM {{{0}}};
            BEGIN
            WHILE 1 DO BEGIN
            END;
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_not_boolean_if_else_condition_raises_compiler_error():
        code = ("expected boolean expression", "", """
            PROGRAM {{{0}}};
            BEGIN
            IF 1 THEN BEGIN
            END ELSE
            BEGIN
            END;
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_reference_to_unknown_procedure_raises_compiler_error():
        code = ("Unknown procedure", "", """
            PROGRAM {{{0}}};
            BEGIN
                A_PROCEDURE(1);
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_type_identifier_already_declared_raises_compiler_error():
        code = ("already declared", "", """
            PROGRAM {{{0}}};
            TYPE
                T1 = INTEGER;
                T1 = REAL;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_reference_to_unknown_type_identifier_raises_compiler_error():
        code = ("reference to unknown type", "", """
            PROGRAM {{{0}}};
            TYPE
                T1 = AN_UNDECLARED_TYPE;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_large_hexadecimal_number_raises_compiler_error():
        code = ("not compatible with type limitations", "", """
            PROGRAM {{{0}}};
            CONST
                C1 = &HFFFFF;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_large_octal_number_raises_compiler_error():
        code = ("not compatible with type limitations", "", """
            PROGRAM {{{0}}};
            CONST
                C1 = &O1777777;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_large_binary_number_raises_compiler_error():
        code = ("not compatible with type limitations", "", """
            PROGRAM {{{0}}};
            CONST
                C1 = &B10000000000000000;
            BEGIN
            END.                                                   
        """)
        return code

