
class TestSuit:

    @staticmethod
    def generator_tests_to_run():
        return [
            ["scenario_fahrenheit_to_celsius_converter", TDD().scenario_fahrenheit_to_celsius_converter()],

        ]

    @staticmethod
    def parser_tests_to_run():
        return [
            ["scenario_fahrenheit_to_celsius_converter", TDD().scenario_fahrenheit_to_celsius_converter()],

        ]

    @staticmethod
    def compiler_tests_to_run():
        return [
            ["scenario_fahrenheit_to_celsius_converter", TDD().scenario_fahrenheit_to_celsius_converter()],

        ]

    @staticmethod
    def tests_to_run():
        return [
    ["tdd_1", TDD().tdd_1()],
    ["tdd_2", TDD().tdd_2()],
    ["scenario_fahrenheit_to_celsius_converter", TDD().scenario_fahrenheit_to_celsius_converter()],
    ["scenario_program_definition_with_variables", LanguageTests().scenario_program_definition_with_variables()],
    ["scenario_program_definition_without_variables", LanguageTests().scenario_program_definition_without_variables()],
    ["scenario_label_declaration", LanguageTests().scenario_label_declaration()],
    ["scenario_decimal_numbers", LanguageTests().scenario_decimal_numbers()],
    ["scenario_binary_numbers", LanguageTests().scenario_binary_numbers()],
    ["scenario_octal_numbers", LanguageTests().scenario_octal_numbers()],
    ["scenario_hexadecimal_numbers", LanguageTests().scenario_hexadecimal_numbers()],
    ["scenario_strings", LanguageTests().scenario_strings()],
    ["scenario_booleans", LanguageTests().scenario_booleans()],
    ["scenario_constant_declaration", LanguageTests().scenario_constant_declaration()],
    ["scenario_type_declaration_with_base_types", LanguageTests().scenario_type_declaration_with_base_types()],
    ["scenario_type_declaration_with_pointer_to_base_types", LanguageTests().scenario_type_declaration_with_pointer_to_base_types()],
    ["scenario_type_declaration_with_declared_types", LanguageTests().scenario_type_declaration_with_declared_types()],
    ["scenario_variable_declaration_with_base_types", LanguageTests().scenario_variable_declaration_with_base_types()],
    ["scenario_variable_declaration_with_types_based_on_base_types", LanguageTests().scenario_variable_declaration_with_types_based_on_base_types()],
    ["scenario_variable_declaration_with_pointers_to_base_types", LanguageTests().scenario_variable_declaration_with_pointers_to_base_types()],
    ["scenario_variable_declaration_with_pointer_to_pointer_types", LanguageTests().scenario_variable_declaration_with_pointer_to_pointer_types()],
    ["scenario_variable_declaration_with_pointer_types_based_on_base_types", LanguageTests().scenario_variable_declaration_with_pointer_types_based_on_base_types()],
    ["scenario_variable_assignment_with_nil", LanguageTests.scenario_variable_assignment_with_nil()],
    ["scenario_variable_assignment_with_single_value", LanguageTests().scenario_variable_assignment_with_single_value()],
    ["scenario_variable_assignment_with_constant", LanguageTests().scenario_variable_assignment_with_constant()],
    ["scenario_variable_assignment_with_variable", LanguageTests().scenario_variable_assignment_with_variable()],
    ["scenario_variable_assignment_with_numeric_expression", LanguageTests().scenario_variable_assignment_with_numeric_expression()],
    ["scenario_variable_assignment_with_logical_expression_same_types", LanguageTests().scenario_variable_assignment_with_logical_expression_same_types()],
    ["scenario_variable_assignment_with_logical_expression_mixed_types", LanguageTests().scenario_variable_assignment_with_logical_expression_mixed_types()],
    ["scenario_repeat_loop_with_boolean_constant", LanguageTests().scenario_repeat_loop_with_boolean_constant()],
    ["scenario_repeat_loop_with_boolean_expression", LanguageTests().scenario_repeat_loop_with_boolean_expression()],
    ["scenario_repeat_loop_with_variable", LanguageTests().scenario_repeat_loop_with_variable()],
    ["scenario_repeat_loop_with_expression", LanguageTests().scenario_repeat_loop_with_expression()],
    ["scenario_for_to_loop_with_constants", LanguageTests.scenario_for_to_loop_with_constants()],
    ["scenario_for_to_loop_with_expressions", LanguageTests.scenario_for_to_loop_with_expressions()],
    ["scenario_for_to_loop_with_begin_end", LanguageTests.scenario_for_to_loop_with_begin_end()],
    ["scenario_for_downto_loop_with_constants", LanguageTests.scenario_for_downto_loop_with_constants()],
    ["scenario_for_downto_loop_with_expressions", LanguageTests.scenario_for_downto_loop_with_expressions()],
    ["scenario_for_downto_loop_with_begin_end", LanguageTests.scenario_for_downto_loop_with_begin_end()],
        ]


class LanguageTests(TestSuit):

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
    def scenario_decimal_numbers():
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
    def scenario_binary_numbers():
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
    def scenario_octal_numbers():
        code = """
            PROGRAM {{{0}}};                 
            CONST                                    
            C1 = &O00;                               
            C2 = &o00;                               
            C3 = &O01234567;                         
            C4 = &O01234567;                         
            BEGIN                                    
            END.                                   
        """
        return code


    @staticmethod
    def scenario_hexadecimal_numbers():
        code = """
            PROGRAM {{{0}}};                 
            CONST                                    
            C1 = &h00;                               
            C2 = &H00;                               
            C3 = &hABCDFE;                           
            C4 = &HABCDFE;                           
            C5 = &h0123456789;                       
            C6 = &H0123456789;                       
            C7 = &H0123456789ABCDEF;                 
            C8 = &h0123456789ABCDEF;                 
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
            BEGIN                                    
            END.                                   
        """
        return code


    @staticmethod
    def scenario_constant_declaration():
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
            C5 = 'C';                                
            C6 = 'C8C8C8C8';                         
            C7 = True;                               
            C8 = False;                              
            C9 = Nil;                             
            BEGIN                                   
            END.                                  
        """
        return code

    @staticmethod
    def scenario_type_declaration_with_base_types():
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
    def scenario_type_declaration_with_pointer_to_base_types():
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
    def scenario_type_declaration_with_declared_types():
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
    def scenario_variable_declaration_with_base_types():
        code = """
            PROGRAM {{{0}}};   
            VAR V1, V2 : INTEGER;
                _V3    : REAL;                    
                _V4  : BOOLEAN;                 
                _V5  : CHAR;                    
                _V6  : STRING;                 
                _V7  : TEXT;                   
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_declaration_with_pointers_to_base_types():
        code = """
            PROGRAM {{{0}}};   
            VAR V1, V2 : ^INTEGER;
                V3    : ^REAL;                    
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
            VAR V1, V2  : T1;                 
                V3      : T2;                    
                V4      : T3;                 
                V5      : T4;                    
                V6      : T5;                 
                V7      : T6;                         
                V8      : ^T1;               
                V9, V10 : ^T2;
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
            VAR V1, V2 : ^T1;                 
                _V4    : ^T2;                    
                _V5  : ^T3;                 
                _V6  : ^T4;                    
                _V7  : ^T5;                 
                _V8  : ^T6;                         
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
            VAR V1, V2 : ^T1;                 
                _V3    : ^T2;                    
                _V4  : ^T3;                 
                _V5  : ^T4;                    
                _V6  : ^T5;                 
                _V7  : ^T6;                         
            BEGIN                                 
            END.                                  
        """
        return code

    @staticmethod
    def scenario_variable_assignment_with_nil():
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
            V4 := NIL;                               
            V5 := NIL;                               
            V7 := NIL;                               
            V8 := NIL;
            V9 := NIL;                               
            V10 := NIL;                               
            V11 := NIL;                               
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
             V5 : STRING;                         
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
            END.                                   
        """
        return code


    @staticmethod
    def scenario_variable_assignment_with_constant():
        code = """
            PROGRAM {{{0}}};                 
            CONST C1 = NIL;
                  C2 = 'C';                                
                  C3 = 'C8C8C8C8';                         
                  C4 = TRUE;
                  C5 = 123;
            VAR V1 : ^INTEGER;
                V2 : CHAR;
                V3 : STRING;
                V4 : BOOLEAN;
                V5 : INTEGER;                         
            BEGIN                                     
             V1 := C1;
             V2 := C2;
             V3 := C3;
             V4 := C4;
             V5 := C5;
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
             V1 := V1 and True or (V2 > 1) and (not ((V1 <> False) and (V1 = True) and (-2.0 >= V3)));              
            END.                                      
        """
        return code

    @staticmethod
    def scenario_variable_assignment_with_logical_expression_mixed_types():
        code = """
            PROGRAM {{{0}}};                  
            VAR V1 : BOOLEAN;   
             V2 : INTEGER;                     
            BEGIN           
             V2 := 0;                          
             V1 := V1 and True or V1 and (not (V2 >= 1));              
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
            VAR X : INTEGER;                             
            BEGIN                                        
               FOR X := 1 TO 10 DO                       
                  V1 := X;                               
            END.                                       
        """
        return code

    @staticmethod
    def scenario_for_to_loop_with_expressions():
        code = """
            PROGRAM {{{0}}};                   
            VAR V1 : INTEGER;                              
            BEGIN                                          
               FOR X := (1 + 2 * 3) TO (10 + 1 * 2) DO     
                  V1 := X;                                 
            END.                                         
        """
        return code


    @staticmethod
    def scenario_for_to_loop_with_begin_end():
        code = """
            PROGRAM {{{0}}};                 
            VAR V1 : INTEGER;                            
            BEGIN                                        
               FOR X := 1 TO 10 DO                       
                  BEGIN                                  
                     V1 := X;                            
                  END;                                   
            END.                                       
        """
        return code


    @staticmethod
    def scenario_for_downto_loop_with_constants():
        code = """
            PROGRAM {{{0}}};                 
            VAR V1 : INTEGER;                            
            BEGIN                                        
               FOR X := 10 DOWNTO 1 DO                   
                  V1 := X;                               
            END.                                       
        """
        return code

    @staticmethod
    def scenario_for_downto_loop_with_expressions():
        code = """
            PROGRAM {{{0}}};                   
            VAR V1 : INTEGER;                              
            BEGIN                                          
               FOR X := (1 + 2 * 3) DOWNTO (10 + 1 * 2) DO     
                  V1 := X;                                 
            END.                                         
        """
        return code

    @staticmethod
    def scenario_for_downto_loop_with_begin_end():
        code = """
            PROGRAM {{{0}}};                 
            VAR V1 : INTEGER;                            
            BEGIN                                        
               FOR X := 10 DOWNTO 1 DO                   
                  BEGIN                                  
                     V1 := X;                            
                  END;                                   
            END.                                       
        """
        return code


class TDD(TestSuit):

    @staticmethod
    def tdd_1():
        code = """
            PROGRAM {{{0}}};                 
            VAR                                      
            V1 : INTEGER;                            
            BEGIN                                    
            V1 := 1;                                    
            END.                                   
        """
        return code

    @staticmethod
    def tdd_2():
        code = """
            PROGRAM my_test_program( A1, A2, A3);    
            LABEL 100, 200, 300, 400;                
            CONST                                    
            C1 = 0.5;  B = 1;                                
            VAR V1, V3 : INTEGER;                        
            V2 : BOOLEAN;                            
            BEGIN                                    
               REPEAT                                
                 V1 := V1 + 1                      
               UNTIL V1 + V3 > 10 + 1         
            END.                                   
        """
        return code

    @staticmethod
    def scenario_program_definition_2():
        code = """
            program test;                          
            const                                 
              PI = 3.1415;                        
                                                  
            var                                   
              a, b: real;                         
              c : MEUTIPO;                        
            procedure hello(s: string; n: real);  
            begin                                 
              writeln(s);                         
            end;                                  
                                                  
            begin                                 
              a := PI;                            
              b := a * 10;                        
              hello('Hello World!', b);           
            end.                                 
        """
        return code

    @staticmethod
    def scenario_fahrenheit_to_celsius_converter():
        code = """
            program {{{0}}}(output);
            { Program to convert temperatures from
             Fahrenheit to Celsius. }
            const
                MIN = 0;
                MAX = 300;
            var
                fahren: integer;
                celsius: real;
            begin
                writeln('Fahrenheit     Celsius');
                writeln('----------     -------');
                for fahren := MIN to MAX do begin
                    celsius := 5 * (fahren - 32) / 9;
                    writeln(fahren:5, celsius) ;
                end ;               
            end.
        """
        return code
