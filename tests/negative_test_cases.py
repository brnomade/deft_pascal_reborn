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
        return [i for i in inspect.getmembers(cls, predicate=inspect.isfunction) if 'scenario_' in i[0]]

    @staticmethod
    def syntax_error_raises_parser_error_unexpected_token():
        code = """
            PROGRAM {{{0}}}        
            BEGIN                               
            END.                                
        """
        return code

    @staticmethod
    def syntax_error_raises_parser_error_unexpected_characters():
        code = """ "
            PROGRAM {{{0}}}        
            BEGIN                               
            END.                                
        """
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_basic_type_case():
        code = ("incompatible types in expression", """
            PROGRAM {{{0}}};        
            VAR V1 : INTEGER;
            BEGIN
                V1 := True;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_case():
        code = ("incompatible types in expression", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
            BEGIN
                V1 := True;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_dereferencing_at_left():
        code = ("incompatible types in expression", """
            PROGRAM {{{0}}};        
            VAR V1 : ^INTEGER;
            BEGIN
                V1^ := True;                        
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_incompatible_types_assignment_raises_compiler_error_pointer_type_dereferencing_at_right():
        code = ("incompatible types in expression", """
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
        code = ("incompatible types in expression", """
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
        code = ("incompatible types in expression", """
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
        code = ("incompatible types in expression", """
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
        code = ("incompatible types in expression", """
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
        code = ("incompatible types in expression", """
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
        code = ("incompatible types in expression", """
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
        code = ("already declared", """
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
        code = ("invalid assignment to constant", """
            PROGRAM {{{0}}};
            CONST
            C1 = True;
            BEGIN
            C1 := False;
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_variable_identifier_already_declared_raises_compiler_error():
        code = ("already declared", """
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
        code = ("Reference to undeclared", """
            PROGRAM {{{0}}};        
            BEGIN
            V1 := True
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_variable_identifier_declared_with_undeclared_type_raises_compiler_error():
        code = ("unknown type", """
            PROGRAM {{{0}}};        
            VAR
            V1 : AN_UNDECLARED_TYPE;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_reference_to_undeclared_variable_identifier_raises_compiler_error():
        code = ("Reference to undeclared", """
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
        code = ("expected boolean expression", """
            PROGRAM {{{0}}};
            BEGIN
            REPEAT
            UNTIL 1;
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_not_boolean_while_do_condition_raises_compiler_error():
        code = ("expected boolean expression", """
            PROGRAM {{{0}}};
            BEGIN
            WHILE 1 DO BEGIN
            END;
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_not_boolean_if_else_condition_raises_compiler_error():
        code = ("expected boolean expression", """
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
        code = ("Unknown procedure", """
            PROGRAM {{{0}}};
            BEGIN
                A_PROCEDURE(1);
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_type_identifier_already_declared_raises_compiler_error():
        code = ("already declared", """
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
        code = ("reference to unknown type", """
            PROGRAM {{{0}}};
            TYPE
                T1 = AN_UNDECLARED_TYPE;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_large_hexadecimal_number_raises_compiler_error():
        code = ("not compatible with type limitations", """
            PROGRAM {{{0}}};
            CONST
                C1 = &HFFFFF;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_large_octal_number_raises_compiler_error():
        code = ("not compatible with type limitations", """
            PROGRAM {{{0}}};
            CONST
                C1 = &O1777777;
            BEGIN
            END.                                                   
        """)
        return code

    @staticmethod
    def scenario_large_binary_number_raises_compiler_error():
        code = ("not compatible with type limitations", """
            PROGRAM {{{0}}};
            CONST
                C1 = &B10000000000000000;
            BEGIN
            END.                                                   
        """)
        return code
