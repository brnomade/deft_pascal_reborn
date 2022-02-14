"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

import inspect


class PositiveLanguageTests:

    @classmethod
    def available_tests(cls):
        return [i for i in inspect.getmembers(cls, predicate=inspect.isfunction) if 'scenario_' in i[0]]

    @staticmethod
    def scenario_program_definition_without_variables():
        code = """
            PROGRAM {{{0}}};        
            BEGIN                               
            END.                                
        """
        return code

    @staticmethod
    def scenario_program_definition_with_variables():
        code = """
            PROGRAM {{{0}}}( A1, A2, A3);    
            BEGIN                                        
            END.                                       
        """
        return code


    @staticmethod
    def scenario_label_declaration():
        code = """
            PROGRAM {{{0}}}( A1, A2, A3);    
            LABEL 100, 200, 300, 400;                
            BEGIN                                    
            END.                                   
        """
        return code


    @staticmethod
    def scenario_numbers_decimal():
        code = """
            PROGRAM {{{0}}};                 
            CONST                                    
            C1 = 0;                                  
            C2 = +0;                                 
            C3 = -1;                                 
            C4 = +1;                                 
            C5 = -0.5;                               
            C6 = +0.5;                               
            C7 = 0.5e1;                              
            C8 = 0.5E1;                              
            C9 = -0.5E+1;                            
            C10 = +0.5E-1;                           
            BEGIN                                    
            END.                                   
        """
        return code


    @staticmethod
    def scenario_numbers_binary():
        code = """
            PROGRAM {{{0}}};                 
            CONST                                    
            C1 = &B00;                               
            C2 = &b11;                               
            C3 = &B101010101010;                     
            C4 = &b101010101010;                     
            BEGIN                                    
            END.                                   
        """
        return code


    @staticmethod
    def scenario_numbers_octal():
        code = """
            PROGRAM {{{0}}};                 
            CONST                                    
            C1 = &O00;                               
            C2 = &o00;                               
            C3 = &O01267;                         
            C4 = &o177777;                         
            BEGIN                                    
            END.                                   
        """
        return code


    @staticmethod
    def scenario_numbers_hexadecimal():
        code = """
            PROGRAM {{{0}}};                 
            CONST                                    
            C1 = &h00;                               
            C2 = &H00;                               
            C3 = &HAAAA;                           
            C4 = &HBBBB;                           
            C5 = &hCCCC;                       
            C6 = &HDDDD;                       
            C7 = &HEEEE;                 
            C8 = &hFFFF;                 
            BEGIN                                    
            END.                                   
        """
        return code


    @staticmethod
    def scenario_strings():
        code = """
            PROGRAM {{{0}}};                 
            CONST                                    
            C7 = 'C';                                
            C8 = 'C8C8C8C8';                         
            BEGIN                                    
            END.                                   
        """
        return code


    @staticmethod
    def scenario_booleans():
        code = """
            PROGRAM {{{0}}};                 
            CONST                                    
            C1 = True;                               
            C2 = False;                             
            C3 = TRUE;                               
            C4 = FALSE;                             
            C5 = true;                               
            C6 = false;                             
            C7 = TrUe;                               
            C8 = fAlSe;                             
            VAR
            V1 : BOOLEAN;
            BEGIN                
            V1 := True;                               
            V1 := False;                             
            V1 := TRUE;                               
            V1 := FALSE;                             
            V1 := true;                               
            V1 := false;                             
            V1 := TrUe;                               
            V1 := fAlSe;                                               
            END.                                   
        """
        return code


    @staticmethod
    def scenario_constant_declaration_with_nil():
        #code = """
        #    PROGRAM {{{0}}};
        #    CONST
        #    C1 = Nil;
        #    C2 = C1;
        #    BEGIN
        #    END.
        print("WARNING - scenario_constant_declaration_with_nil - test still not passing - code needs review...")
        code = """
            PROGRAM {{{0}}};                
            BEGIN                                   
            END.                                  
        """
        return code

    @staticmethod
    def scenario_constant_declaration_with_string_literal():
        code = """
            PROGRAM {{{0}}};                
            CONST                                   
            C1 = 'C';                                
            C2 = 'C8C8C8C8';                         
            BEGIN                                   
            END.                                  
        """
        return code

    @staticmethod
    def scenario_constant_declaration_with_single_value_string_constant():
        code = """
            PROGRAM {{{0}}};                
            CONST                                   
            C1 = 'C';                                
            C5 = C1;                                
            C2 = 'C8C8C8C8';                         
            C6 = C2;                         
            BEGIN        
                WRITELN(C1);
                WRITELN(C5);
                WRITELN(C2);
                WRITELN(C6);                           
            END.                                  
        """
        return code

    @staticmethod
    def scenario_constant_declaration_with_expression_string_constant():
        code = """
            PROGRAM {{{0}}};                
            CONST                                   
            C1 = 'C';                                
            C5 = C1 + C1 + 'C';                                
            C2 = 'C8C8C8C8';                         
            C6 = C2 + C2 + 'C9C9C9C9';                         
            BEGIN        
                WRITELN(C1);
                WRITELN(C5);
                WRITELN(C2);
                WRITELN(C6);                           
            END.                                  
        """
        return code

    @staticmethod
    def scenario_constant_declaration_with_single_value():
        code = """
            PROGRAM {{{0}}};                
            CONST                                   
            C1 = 2;                                  
            C1a = -1;                                 
            C1b = +1;                                 
            C2 = 1.0;                                
            C2a = -1.0;                               
            C2b = +1.0;                               
            C3 = 1.0e-12;                            
            C3a = -1.0e+12;                            
            C3b = 1.0e12;                            
            C4 = &HFF;                               
            C4a = &B10;                               
            C4b = &O12;                               
            C7 = True;                               
            C8 = False;                              
            BEGIN                                   
            END.                                  
        """
        return code

    @staticmethod
    def scenario_constant_declaration_with_value_based_expression():
        code = """
            PROGRAM {{{0}}};                
            CONST                                   
            C1 = 2 + 2;                                  
            C1a = -1 - 1;                                 
            C1b = +1 + 1;                                 
            C2 = 1.0 / ( 1.0 + 1.0 - 1.0 * 1.0 + (1.0 * 1.0));                                
            C2a = -1.0 / 1.0;                               
            C2b = +1.0 / 1.0;                               
            C3 = 1.0e-12 + 1.0e-12;                            
            C3a = -1.0e+12 - 1.0e-12;                            
            C3b = 1.0e12 / 1.0e-12;                            
            C4 = &HFF + &HFF;                               
            C4a = &B10 + &B10;                               
            C4b = &O12 - &O12;                               
            C7 = (True and (False or not True)) and (true and not (true or false));                               
            C8 = False and (False or not True);                              
            BEGIN                                   
            END.                                  
        """
        return code

    @staticmethod
    def scenario_constant_declaration_with_identifier_based_expression():
        code = """
            PROGRAM {{{0}}};                
            CONST                                   
            C1 = 2 + 2;                                  
            C1a = -1 - C1;                                 
            C1b = +1 + C1a;                                 
            C2 = 1.0 / C1;                                
            C2a = -1.0 / C2;                               
            C2b = +1.0 / C2a;                               
            C3 = 1.0e-12 + 1.0e-12;                            
            C3a = -1.0e+12 - 1.0e-12;                            
            C3b = 1.0e12 / 1.0e-12;                            
            C4 = &HFF + &HFF;                               
            C4a = &B10 + &B10;                               
            C4b = &O12 - &O12;      
            C6 = True;
            C7 = False;                         
            C8 = (C6 and C7) or not C6;                               
            C9 = (C7 and C7) or not ((C6 OR C7) and C8);                              
            BEGIN       
                writeln(C1);                            
                writeln(C1a);                            
                writeln(C1b);                            
                writeln(C2);                            
                writeln(C2a);                            
                writeln(C2b);                            
                writeln(C3);                            
                writeln(C3a);                            
                writeln(C3b);                            
                writeln(C4);                            
                writeln(C4a);                            
                writeln(C4b);                            
                writeln(C6);                            
                writeln(C7);                            
                writeln(C8);                            
                writeln(C9);                            
            END.                                  
        """
        return code

    @staticmethod
    def scenario_type_definition_with_base_types():
        code = """
            PROGRAM {{{0}}};          
            TYPE
                T1 = INTEGER;
                T2 = REAL;
                T3 = CHAR;
                T4 = STRING;
                T5 = BOOLEAN;
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_type_definition_with_pointer_to_base_types():
        code = """
            PROGRAM {{{0}}};          
            TYPE
                T6 = ^INTEGER;
                T7 = ^REAL; 
                T8 = ^CHAR;
                T9 = ^STRING;
                T10 = ^BOOLEAN;  
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_type_definition_with_declared_types():
        code = """
            PROGRAM {{{0}}};          
            TYPE
                T1 = INTEGER;
                T2 = REAL;
                T3 = CHAR;
                T4 = STRING;
                T5 = BOOLEAN;
                T6 = ^INTEGER;
                T7 = ^REAL; 
                T8 = ^CHAR;
                T9 = ^STRING;
                T10 = ^BOOLEAN;  
                T11 = T1;
                T12 = T6;
                T13 = T12;
                T14 = ^T12;     
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_declaration_multiple_variables_declared():
        code = """
            PROGRAM {{{0}}};   
            VAR V1, V2, V3, V4, V5 : INTEGER;
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_declaration_with_base_types():
        code = """
            PROGRAM {{{0}}};   
            VAR V1  : INTEGER;
                V3  : REAL;                    
                V4  : BOOLEAN;                 
                V5  : CHAR;                    
                V6  : STRING;  
                V6_b : STRING(255);               
                V7  : TEXT;                   
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_declaration_with_pointers_to_base_types():
        code = """
            PROGRAM {{{0}}};   
            VAR V1  : ^INTEGER;
                V3  : ^REAL;                    
                V4  : ^BOOLEAN;                 
                V5  : ^CHAR;                    
                V6  : ^STRING;                 
                V7  : ^TEXT;                   
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_declaration_with_types_based_on_base_types():
        code = """
            PROGRAM {{{0}}};          
            TYPE
                T1 = INTEGER;
                T2 = REAL;
                T3 = BOOLEAN;
                T4 = CHAR;
                T5 = STRING;
                T6 = TEXT;
            VAR V1   : T1;                 
                V2   : T2;                    
                V3   : T3;                 
                V4   : T4;                    
                V5   : T5;                 
                V6   : T6;                         
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_declaration_with_pointer_types_based_on_base_types():
        code = """
            PROGRAM {{{0}}};          
            TYPE
                T1 = INTEGER;
                T2 = REAL;
                T3 = BOOLEAN;
                T4 = CHAR;
                T5 = STRING;
                T6 = TEXT;
            VAR _V1 : ^T1;     
                _V2 : ^T2;                    
                _V3 : ^T3;                 
                _V4 : ^T4;                    
                _V5 : ^T5;                 
                _V6 : ^T6;                         
            BEGIN        
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_declaration_with_pointer_to_pointer_types():
        code = """
            PROGRAM {{{0}}};          
            TYPE
                T1 = ^INTEGER;
                T2 = ^REAL;
                T3 = ^BOOLEAN;
                T4 = ^CHAR;
                T5 = ^STRING;
                T6 = ^TEXT;
            VAR V1  : ^T1;                 
                V3  : ^T2;                    
                V4  : ^T3;                 
                V5  : ^T4;                    
                V6  : ^T5;                 
                V7  : ^T6;                         
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_assignment_with_nil():
        # on this test, following lines still give errors:
        #            V4 := NIL;
        #            V7 := NIL;
        #            V9 := NIL;
        #            V11 := NIL;
        print("WARNING - scenario_variable_assignment_with_nil - test still not passing - code needs review...")
        code = """
            PROGRAM {{{0}}};  
            TYPE
                T1 = ^INTEGER;
                T2 = INTEGER;   
                T4 = T1;
                T5 = ^T1;
                T6 = ^T2;     
            VAR                                     
            V1 : ^INTEGER;  
            V3 : ^T1;
            V4 : T1;
            V5 : ^T2;
            V7 : T4;
            V8 : ^T4;
            V9 : T5;
            V10: ^T5;
            V11: T6;
            V12: ^T6;
            BEGIN                                   
            V1 := NIL;
            V3 := NIL;                               
            V5 := NIL;                               
            V8 := NIL;
            V10 := NIL;                               
            V12 := NIL;        
            END.                                    
        """
        return code


    @staticmethod
    def scenario_variable_assignment_with_single_value():
        code = """
            PROGRAM {{{0}}};                 
            VAR                                    
             V1 : INTEGER;                                
             V2 : BOOLEAN;                             
             V3 : CHAR;                              
             V4 : STRING;                         
             V6 : INTEGER;                               
             V7 : REAL;                             
             V8 : INTEGER;                             
             V9 : INTEGER;                             
             V10 : INTEGER;                           
             V12 : REAL;                             
            BEGIN                   
             V1 := -2;                                
             V2 := False;                             
             V3 := 'C';                              
             V4 := 'STRING';                         
             V6 := -1;                               
             V7 := -1.0;                             
             V8 := &HFF;                             
             V9 := &B10;                             
             V10 := &O11;                            
             V12 := -1.1E-23;     
             WRITELN(V1);
             WRITELN(V2);
             WRITELN(V3);
             WRITELN(V4);
             WRITELN(V6);
             WRITELN(V7);
             WRITELN(V8);
             WRITELN(V9);
             WRITELN(V10);
             WRITELN(V12);                    
            END.                                   
        """
        return code

    @staticmethod
    def scenario_variable_assignment_with_constant():
        code = """
            PROGRAM {{{0}}};                 
            CONST C2 = 'C';                                
                  C3 = 'C8C8C8C8';                         
                  C4 = TRUE;
                  C5 = 123;
            VAR V2 : CHAR;
                V3 : STRING;
                V4 : BOOLEAN;
                V5 : INTEGER;                         
            BEGIN                                     
             V2 := C2;
             V3 := C3;
             V4 := C4;
             V5 := C5;
            END.                                      
        """
        return code

    @staticmethod
    def scenario_pointer_variable_assignment_with_constant():
        # code = """
        #     PROGRAM {{{0}}};
        #     CONST C1 = NIL;
        #     VAR V1 : ^INTEGER;
        #     BEGIN
        #      V1 := C1;
        #      V1 := NIL;
        #     END.
        # """
        print("WARNING - scenario_pointer_variable_assignment_with_constant - test still not passing - code needs review...")
        code = """
            PROGRAM {{{0}}};                
            BEGIN                                   
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_assignment_with_variable():
        code = """
            PROGRAM {{{0}}};                 
            VAR V1, V2 : INTEGER;
            BEGIN                                     
             V1 := V1;
             V1 := V2;
            END.                                      
        """
        return code

    @staticmethod
    def scenario_variable_assignment_with_pointer():
        # code = """
        #     PROGRAM {{{0}}};
        #     VAR V1 : ^INTEGER;
        #         V2 : ^INTEGER;
        #         V3 : INTEGER;
        #         V4 : ^STRING(50);
        #     BEGIN
        #      V1^ := 10;
        #      V2^ := 20;
        #      V3 := 30;
        #      V4^ := 'ABCDEFE';
        #      V1 := V2;
        #      V1^ := V2^;
        #      V1^ := V3;
        #     END.
        # """
        print("WARNING - scenario_variable_assignment_with_pointer - test still not passing - code needs review...")
        code = """
            PROGRAM {{{0}}};                
            BEGIN                                   
            END.                                  
        """
        return code


    @staticmethod
    def scenario_variable_assignment_with_numeric_expression():
        code = """
            PROGRAM {{{0}}};                  
            VAR V1 : INTEGER;                         
                V2 : REAL;                         
            BEGIN                                     
             V1 := 2 + V1 * -3 + (2.0 DIV &HFF);              
             V2 := 2.0 + V2 * -3.0 + (255 / 2.0);
             V2 := -2.0 + V2 * 3.0 + (1.0 / -1.1E-23 * (V2 + 1.0 + -1.0))
            END.                                      
        """
        return code

    @staticmethod
    def scenario_variable_assignment_with_logical_expression_same_types():
        code = """
            PROGRAM {{{0}}};                  
            VAR V1 : BOOLEAN;   
            V2 : INTEGER;
            V3 : REAL;
            BEGIN           
             V1 := ((V1 and True) or (V2 > 1)) and (not ((V1 <> False) and (V1 = True) and (-2.0 >= V3)));              
            END.                                      
        """
        return code

    @staticmethod
    def scenario_variable_assignment_with_logical_expression_mixed_types():
        code = """
            PROGRAM {{{0}}};                  
            VAR V1, V3 : BOOLEAN;   
             V2 : INTEGER;                     
            BEGIN           
             V2 := 0;                          
             V1 := (V1 and True) or (V1 and (not (V2 >= 1)));              
             V3 := V1 and True or V1 and (not (V2 >= 1));
            END.                                      
        """
        return code

    @staticmethod
    def scenario_semicolon_not_required_for_last_statement():
        code = """
            PROGRAM {{{0}}};  
            VAR v1 : INTEGER;            
            BEGIN                                     
               v1 := 1;
               writeln(v1)
            END. 
        """
        return code

    @staticmethod
    def scenario_semicolon_accepted_for_last_statement():
        code = """
            PROGRAM {{{0}}};  
            VAR v1 : INTEGER;            
            BEGIN                                     
               v1 := 1;
               writeln(v1);
            END. 
        """
        return code

    @staticmethod
    def scenario_repeat_loop_with_boolean_constant():
        code = """
            PROGRAM {{{0}}};  
            VAR v1 : INTEGER;            
            BEGIN                                     
               REPEAT                
               v1 := 1;
               v1 := 2;                 
               UNTIL True                             
            END. 
        """
        return code

    @staticmethod
    def scenario_repeat_loop_with_boolean_expression():
        code = """
            PROGRAM {{{0}}};              
            BEGIN                                     
               REPEAT                                 
               UNTIL True and True                    
            END.                                      
        """
        return code


    @staticmethod
    def scenario_repeat_loop_with_variable():
        code = """
            PROGRAM {{{0}}};     
            VAR             
                V2 : REAL;                         
            BEGIN                                     
               REPEAT     
               UNTIL V2 = 1.0;                              
            END.                                      
        """
        return code


    @staticmethod
    def scenario_repeat_loop_with_expression():
        code = """
            PROGRAM {{{0}}};                  
            VAR V1 : INTEGER;                         
                V2 : INTEGER;                         
            BEGIN                                     
               REPEAT                                 
               UNTIL V2 + 1 > V1 * (V1 + V2)                       
            END. 
        """
        return code

    @staticmethod
    def scenario_for_to_loop_with_constants():
        code = """
            PROGRAM {{{0}}};                 
            VAR V1, V2 : INTEGER;                             
            BEGIN                                        
               FOR V1 := 1 TO 10 DO                       
                  V2 := V1;  
                  writeln(V2)                             
            END.                                       
        """
        return code

    @staticmethod
    def scenario_for_to_loop_with_expressions():
        code = """
            PROGRAM {{{0}}};                   
            VAR V1, V2 : INTEGER;                              
            BEGIN                                          
               FOR V2 := (1 + (2 * 3) + V1) DOWNTO (10 + (1 * 2) + V1) DO     
                  V1 := V2;                                 
            END.                                         
        """
        return code


    @staticmethod
    def scenario_for_to_loop_without_begin_end():
        code = """
            PROGRAM {{{0}}};                 
            VAR V1, V2 : INTEGER;                            
            BEGIN                                        
               FOR V1 := 1 TO 10 DO                       
                  V1 := V2;                                   
            END.                                       
        """
        return code


    @staticmethod
    def scenario_for_downto_loop_with_constants():
        code = """
            PROGRAM {{{0}}};                 
            VAR V1, V2 : INTEGER;                             
            BEGIN                                        
               FOR V1 := 10 DOWNTO 1 DO                       
                  V2 := V1;                               
            END.                                       
        """
        return code

    @staticmethod
    def scenario_for_downto_loop_with_expressions():
        code = """
            PROGRAM {{{0}}};                   
            VAR V1, V2 : INTEGER;                              
            BEGIN                                          
               FOR V2 := (1 + (2 * 3) + V1) DOWNTO (10 + (1 * 2) + V1) DO     
                  V1 := V2;                                 
            END.                                         
        """
        return code

    @staticmethod
    def scenario_for_downto_loop_without_begin_end():
        code = """
            PROGRAM {{{0}}};                 
            VAR V1, V2 : INTEGER;                            
            BEGIN                                        
               FOR V1 := 1 TO 10 DO                       
                  V1 := V2;                                   
            END.             
        """
        return code

    @staticmethod
    def scenario_while_do_loop_with_variable():
        code = """
            PROGRAM {{{0}}};            
            VAR V1, V2 : INTEGER;                            
            BEGIN        
               V1 := 1;                                
               V2 := 10;
               WHILE V1 < V2 DO                   
                  BEGIN                                  
                     V1 := V1 + 1;                            
                  END;                                   
            END.                                       
        """
        return code

    @staticmethod
    def scenario_while_do_loop_with_constant():
        code = """
            PROGRAM {{{0}}};                
            CONST X = 10; 
            VAR V1 : INTEGER;                            
            BEGIN      
               V1 := 1;                                  
               WHILE V1 < X DO                   
                  V1 := V1 + 1;                               
            END.                                       
        """
        return code

    @staticmethod
    def scenario_while_do_loop_with_number():
        code = """
            PROGRAM {{{0}}};                
            VAR V1 : INTEGER;                            
            BEGIN      
               V1 := 1;                                  
               WHILE V1 < 10 DO                   
                  V1 := V1 + 1;                               
            END.                                       
        """
        return code

    @staticmethod
    def scenario_while_do_loop_with_expression():
        code = """
            PROGRAM {{{0}}};                   
            VAR V1 : INTEGER;                              
            BEGIN             
               V1 := 1;                             
               WHILE V1 < (1 + 2 * 3) DO     
                  V1 := V1 + 1;                                 
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_without_parameters_without_directive():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure;
                BEGIN
                    writeln('inside first_procedure');
                END;
            BEGIN             
                writeln('inside main block');
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_without_parameters_without_directive_multiple_declarations_at_same_level():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure;
                BEGIN
                    writeln('inside first_procedure');
                END;
                PROCEDURE second_procedure;
                BEGIN
                    writeln('inside second_procedure');
                END;
                PROCEDURE third_procedure;
                BEGIN
                    writeln('inside third_procedure');
                END;
            BEGIN             
                writeln('inside main block');
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_single_parameter_without_directive():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure( p1 : INTEGER );
                BEGIN
                    writeln('test');
                END;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_parameter_without_directive():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure( p1 : INTEGER; p2 : BOOLEAN; p3 : REAL; p4: STRING; p5 : CHAR );
                BEGIN
                    writeln('test');
                END;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_parameter_same_type_without_directive():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure(p1, p2, p3, p4, p5 : INTEGER);
                BEGIN
                    writeln('test');
                END;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_parameter_same_type_mixed_without_directive():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure(p1, p2: INTEGER; p3, p4, p5 : BOOLEAN);
                BEGIN
                    writeln('test');
                END;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_without_parameters_with_directive_forward():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure; forward;
                PROCEDURE first_procedure;
                BEGIN
                    writeln('first_procedure resolved');
                END;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_without_parameters_with_directive_forward_multiple_list():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure; forward;
                PROCEDURE second_procedure; forward;
                PROCEDURE third_procedure; forward;
                PROCEDURE first_procedure;
                BEGIN
                    writeln('first_procedure resolved');
                END;
                PROCEDURE second_procedure;
                BEGIN
                    writeln('second_procedure resolved');
                END;
                PROCEDURE third_procedure;
                BEGIN
                    writeln('third_procedure resolved');
                END;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_without_parameters_with_directive_forward_multiple_mixed_list():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure; forward;
                PROCEDURE second_procedure; external;
                PROCEDURE third_procedure; forward;
                PROCEDURE fourth_procedure; external;
                PROCEDURE first_procedure;
                BEGIN
                    writeln('first_procedure resolved');
                END;
                PROCEDURE third_procedure;
                BEGIN
                    writeln('third_procedure resolved');
                END;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_single_parameter_with_directive_forward():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure( p1 : integer); forward;
                PROCEDURE first_procedure( p1 : integer);
                BEGIN
                    writeln('first_procedure');
                END;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_parameter_with_directive_forward():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure( p1 : integer; p2 : BOOLEAN; p3 : REAL; p4: STRING; p5 : CHAR ); forward;
                PROCEDURE first_procedure( p1 : integer; p2 : BOOLEAN; p3 : REAL; p4: STRING; p5 : CHAR );
                BEGIN
                    writeln('first_procedure');
                END;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_without_parameters_with_directive_external():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure; external;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_single_parameter_with_directive_external():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure( p1 : integer); external;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_parameter_with_directive_external():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure( p1 : integer; p2 : BOOLEAN; p3 : REAL; p4: STRING; p5 : CHAR ); external;
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_parameter_same_type_mixed_with_directive():
        code = """
            PROGRAM {{{0}}};                   
                PROCEDURE first_procedure(p1, p2: INTEGER; p3, p4, p5 : BOOLEAN; p6 : REAL); forward;
                PROCEDURE first_procedure(p1, p2: INTEGER; p3, p4, p5 : BOOLEAN; p6 : REAL); 
                BEGIN
                    writeln('first_procedure');
                END;
            BEGIN             
            END.                                         
        """
        return code


    @staticmethod
    def scenario_procedure_invocation_single_parameter_with_literal():
        code = """
                PROGRAM {{{0}}};                   
                    PROCEDURE first_procedure(p1 : integer); 
                    BEGIN
                        writeln('first_procedure');
                    END;
                BEGIN             
                    first_procedure(1)
                END.                                         
            """
        return code

    @staticmethod
    def scenario_procedure_invocation_single_parameter_with_variable():
        code = """
                PROGRAM {{{0}}};                   
                    VAR
                        x : integer;
                    PROCEDURE first_procedure(p1 : integer); 
                    BEGIN
                        writeln('first_procedure');
                    END;
                BEGIN             
                    x := 1;
                    first_procedure(x)
                END.                                         
            """
        return code

    @staticmethod
    def scenario_procedure_invocation_single_parameter_with_expression():
        code = """
                PROGRAM {{{0}}};                   
                    VAR
                        x : integer;
                    PROCEDURE first_procedure(p1 : integer); 
                    BEGIN
                        writeln('first_procedure');
                    END;
                BEGIN             
                    x := 1;
                    first_procedure(x + x)
                END.                                         
            """
        return code

    @staticmethod
    def scenario_procedure_declaration_without_parameters():
        code = """
            PROGRAM {{{0}}};                   
            PROCEDURE P1;
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_declaration_without_parameters():
        code = """
            PROGRAM {{{0}}};                   
            FUNCTION F1 : INTEGER;
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_single_static_parameter():
        code = """
            PROGRAM {{{0}}};                                                 
            PROCEDURE P1( SP1 : INTEGER );
            VAR
            P1_V1 : INTEGER;
            BEGIN
            P1_V1 := 0;
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_declaration_with_single_static_parameter():
        code = """
            PROGRAM {{{0}}};                                                 
            FUNCTION F1( SP1 : INTEGER ) : INTEGER ; FORWARD; 
            FUNCTION F1( SP1 : INTEGER ) : INTEGER ;
            VAR
            F1_V1 : INTEGER;
            BEGIN
            F1_V1 := SP1;
            F1 := F1_V1;
            END;            
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_static_parameter_same_type():
        code = """
            PROGRAM {{{0}}};                                                 
            PROCEDURE P1( SP1, SP2 : INTEGER );
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_declaration_with_multiple_static_parameter_same_type():
        code = """
            PROGRAM {{{0}}};                                                 
            FUNCTION F1( SP1, SP2 : INTEGER ) : INTEGER;
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_static_parameter_multiple_types():
        code = """
            PROGRAM {{{0}}};                                                 
            PROCEDURE P1( SP1 : INTEGER; SP2 : BOOLEAN );
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_declaration_with_multiple_static_parameter_multiple_types():
        code = """
            PROGRAM {{{0}}};                                                 
            FUNCTION F1( SP1 : INTEGER; SP2 : BOOLEAN ) : INTEGER;
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_single_variable_parameter():
        code = """
            PROGRAM {{{0}}};                                                 
            PROCEDURE P1( VAR SP1 : INTEGER );
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_declaration_with_single_variable_parameter():
        code = """
            PROGRAM {{{0}}};                                                 
            FUNCTION F1( VAR SP1 : INTEGER ) : INTEGER;
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_variable_parameter_same_type():
        code = """
            PROGRAM {{{0}}};                                                 
            PROCEDURE P1( VAR SP1, SP2 : INTEGER );
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_declaration_with_multiple_variable_parameter_same_type():
        code = """
            PROGRAM {{{0}}};                                                 
            FUNCTION F1( VAR SP1, SP2 : INTEGER ) : INTEGER;
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_declaration_with_multiple_variable_parameter_multiple_types():
        code = """
            PROGRAM {{{0}}};                                                 
            PROCEDURE P1( VAR SP1 : INTEGER; VAR SP2 : BOOLEAN );
            BEGIN
            END;             
            BEGIN             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_declaration_with_multiple_variable_parameter_multiple_types():
        code = """
            PROGRAM {{{0}}};                                                 
            FUNCTION F1( VAR SP1 : INTEGER; VAR SP2 : BOOLEAN ) : INTEGER;
            BEGIN
                writeln("F1");
            END;             
            BEGIN           
                writeln("MAIN");  
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_invocation_without_parameters():
        code = """
            PROGRAM {{{0}}};                                                 
            PROCEDURE P1;
            BEGIN
            END;             
            BEGIN             
               P1;                             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_invocation_without_parameters_without_assignment():
        code = """
            PROGRAM {{{0}}};                                                 
            FUNCTION F1 : INTEGER;
            BEGIN
            END;             
            BEGIN             
               F1;                             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_invocation_without_parameters_with_assignment():
        code = """
            PROGRAM {{{0}}};
            VAR
            V1 : INTEGER;                                                 
            FUNCTION F1 : INTEGER;
            BEGIN
            END;             
            BEGIN             
               V1 := F1;                             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_invocation_with_single_static_parameter():
        code = """
            PROGRAM {{{0}}};                                                 
            PROCEDURE P1( SP1 : INTEGER );
            BEGIN
            END;             
            BEGIN             
               P1(1);                             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_invocation_with_single_static_parameter():
        code = """
            PROGRAM {{{0}}};                                                 
            FUNCTION F1( SP1 : INTEGER ) : INTEGER;
            BEGIN
            END;             
            BEGIN             
               F1(1);                             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_invocation_with_single_static_parameter_and_assignment():
        code = """
            PROGRAM {{{0}}};                                                 
            VAR
            V1 : INTEGER;
            FUNCTION F1( SP1 : INTEGER ) : INTEGER;
            BEGIN
            END;             
            BEGIN             
               V1 := F1(1);                             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_procedure_invocation_with_multiple_static_parameter():
        code = """
            PROGRAM {{{0}}};                                                 
            PROCEDURE P1( SP1, SP2 : INTEGER );
            BEGIN
            END;             
            BEGIN             
               P1(1,2);                             
            END.                                         
        """
        return code

    @staticmethod
    def function_procedure_invocation_with_multiple_static_parameter():
        code = """
            PROGRAM {{{0}}};                                                 
            FUNCTION F1( SP1, SP2 : INTEGER ) : INTEGER;
            BEGIN
            END;             
            BEGIN             
               F1(1,2);                             
            END.                                         
        """
        return code

    @staticmethod
    def scenario_function_invocation_in_expression_with_assignment():
        code = """
            PROGRAM {{{0}}};                                     
            VAR
            V1 : INTEGER;            
            FUNCTION F1( SP1 : INTEGER ) : INTEGER;
            BEGIN
            END;             
            BEGIN             
               V1 := F1(1) + F1(2);                             
            END.                                         
        """
        return code


    @staticmethod
    def scenario_if_with_else_using_begin_end_with_literals():
        code = """
                PROGRAM {{{0}}};                   
                BEGIN             
                    if 2 > 1 then begin
                        writeln('inside if');
                    end else begin
                        writeln('inside else');
                    end;
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_without_else_using_begin_end_with_literals():
        code = """
                PROGRAM {{{0}}};                   
                BEGIN             
                    if 2 > 1 then begin
                        writeln('inside if');
                    end;
                    writeln('outside if')
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_with_else_without_begin_end_with_literals():
        code = """
                PROGRAM {{{0}}};                   
                BEGIN             
                    if 2 > 1 then
                        writeln('inside if')
                    else
                        writeln('inside else');
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_without_else_without_begin_end_with_literals():
        code = """
                PROGRAM {{{0}}};                   
                BEGIN             
                    if 2 > 1 then
                        writeln('inside if');
                    writeln('outside if')
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_with_else_using_begin_end_with_variables():
        code = """
                PROGRAM {{{0}}};                   
                VAR
                    x, y : INTEGER;
                BEGIN             
                    x := 2;
                    y := 1;
                    if x > y then begin
                        writeln('inside if');
                    end else begin
                        writeln('inside else');
                    end;
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_without_else_using_begin_end_with_variables():
        code = """
                PROGRAM {{{0}}};                   
                VAR
                    x, y : INTEGER;
                BEGIN             
                    x := 2;
                    y := 1;
                    if x > y then begin
                        writeln('inside if');
                    end ;
                    writeln('outside if');
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_with_else_without_begin_end_with_variables():
        code = """
                PROGRAM {{{0}}};                   
                VAR
                    x, y : INTEGER;
                BEGIN             
                    x := 2;
                    y := 1;
                    if x > y then
                        writeln('inside if')
                    else
                        writeln('inside else');
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_without_else_without_begin_end_with_variables():
        code = """
                PROGRAM {{{0}}};                   
                VAR
                    x, y : INTEGER;
                BEGIN             
                    x := 2;
                    y := 1;
                    if x > y then
                        writeln('inside if');
                    writeln('outside else')
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_with_else_using_begin_end_with_expressions():
        code = """
                PROGRAM {{{0}}};                   
                VAR
                    x, y : INTEGER;
                BEGIN             
                    x := 2;
                    y := 1;
                    if x + 1 > y + x then begin
                        writeln('inside if');
                    end else begin
                        writeln('inside else');
                    end;
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_without_else_using_begin_end_with_expressions():
        code = """
                PROGRAM {{{0}}};                   
                VAR
                    x, y : INTEGER;
                BEGIN             
                    x := 2;
                    y := 1;
                    if x + 1 > y + x then begin
                        writeln('inside if');
                    end;
                    writeln('outside else');
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_with_else_without_begin_end_with_expressions():
        code = """
                PROGRAM {{{0}}};                   
                VAR
                    x, y : INTEGER;
                BEGIN             
                    x := 2;
                    y := 1;
                    if x + 1 > y + x then
                        writeln('inside if')
                    else
                        writeln('inside else');
                END.                                         
            """
        return code

    @staticmethod
    def scenario_if_without_else_without_begin_end_with_expressions():
        code = """
                PROGRAM {{{0}}};                   
                VAR
                    x, y : INTEGER;
                BEGIN             
                    x := 2;
                    y := 1;
                    if x + 1 > y + x then
                        writeln('inside if');
                    writeln('outside else');
                END.                                         
            """
        return code

    @staticmethod
    def scenario_string_variables_and_string_literals():
        code = """
                PROGRAM {{{0}}};                   
                VAR
                    a, b, c, d, e : STRING(80);
                BEGIN             
                    a := 'THIS IS A STRING';
                    b := a;
                    c := 'THIS STRING' + 'THAT STRING';
                    d := a + b;
                    e := a + 'THIS IS A STRING';
                    writeln('inside else');
                    writeln(a);
                    writeln(b);
                    writeln(c);
                END.                                         
            """
        return code
