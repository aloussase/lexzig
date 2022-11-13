import unittest
from typing import List

from lexzig.lexer import Lexer


class TestLexer(unittest.TestCase):
    lexer = Lexer()

    def run_test(self, *, input: str, expected: List):
        tokens = self.lexer.lex(input)
        tests = expected
        self.assertEqual(len(tests), len(tokens))
        for expected, actual in zip(tests, tokens):
            self.assertEqual(expected['type'], actual.type)
            self.assertEqual(expected['value'], actual.value)

    def test_lexer_can_lex_special_variable_names(self):
        """
        Test that the lexer can lex special variable names.
        """
        self.run_test(
            input=r'''
            @"una variable con espacios"
            @"while"
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'una variable con espacios'},
                {'type': 'IDENT', 'value': 'while'},
            ]
        )

    def test_lexer_can_lex_builtin_functions(self):
        """
        Test that the lexer can lex builtin functions.
        """
        self.run_test(
            input=r'@import("std");',
            expected=[
                {'type': 'BUILTIN_FUNCTION', 'value': 'import'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'STRING', 'value': '"std"'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'SEMICOLON', 'value': ';'},
            ]
        )

    def test_lexer_can_lex_const_variable_declarations(self):
        """
        Test that the lexer can lex constant variable declarations.
        """
        self.run_test(
            input=r"const buffer: [100]u8 = undefined;",
            expected=[
                {'type': 'CONST',   'value': 'const'},
                {'type': 'IDENT',   'value': 'buffer'},
                {'type': 'COLON',   'value': ':'},
                {'type': 'LBRACE',  'value': '['},
                {'type': 'INTEGER', 'value': 100},
                {'type': 'RBRACE',  'value': ']'},
                {'type': 'TYPE_U8', 'value': 'u8'},
                {'type': 'EQUAL',   'value': '='},
                {'type': 'TYPE_UNDEFINED', 'value': 'undefined'},
                {'type': 'SEMICOLON', 'value': ';'},
            ]
        )

    def test_lexer_can_lex_variable_declarations(self):
        """
        Test that the lexer can lex variable declarations.
        """
        self.run_test(
            input=r'var name = "John Doe";',
            expected=[
                {'type': 'VAR',       'value': 'var'},
                {'type': 'IDENT',     'value': 'name'},
                {'type': 'EQUAL',     'value': '='},
                {'type': 'STRING',    'value': '"John Doe"'},
                {'type': 'SEMICOLON', 'value': ';'},
            ]
        )

    def test_lexer_can_lex_if_expressions(self):
        """
        Test that the lexer can lex if expressions.
        """
        self.run_test(
            input="if (9 < 10) { return 42; } else { return 69; }",
            expected=[
                {'type': 'IF', 'value': 'if'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'INTEGER', 'value': 9},
                {'type': 'LT', 'value': '<'},
                {'type': 'INTEGER', 'value': 10},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'RETURN', 'value': 'return'},
                {'type': 'INTEGER', 'value': 42},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'RCURLY', 'value': '}'},
                {'type': 'ELSE', 'value': 'else'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'RETURN', 'value': 'return'},
                {'type': 'INTEGER', 'value': 69},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'RCURLY', 'value': '}'},
            ]
        )

    def test_lexer_can_lex_switch_expressions(self):
        """
        Test that the lexer can lex switch expressions.
        """
        self.run_test(
            input='''
            var x = switch (10) {
                10, 100 => @divExact(10, 10),
                else => 10,
            };
            ''',
            expected=[
                {'type': 'VAR', 'value': 'var'},
                {'type': 'IDENT', 'value': 'x'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'SWITCH', 'value': 'switch'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'INTEGER', 'value': 10},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'INTEGER', 'value': 10},
                {'type': 'COMMA', 'value': ','},
                {'type': 'INTEGER', 'value': 100},
                {'type': 'FAT_ARROW', 'value': '=>'},
                {'type': 'BUILTIN_FUNCTION', 'value': 'divExact'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'INTEGER', 'value': 10},
                {'type': 'COMMA', 'value': ','},
                {'type': 'INTEGER', 'value': 10},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'ELSE', 'value': 'else'},
                {'type': 'FAT_ARROW', 'value': '=>'},
                {'type': 'INTEGER', 'value': 10},
                {'type': 'COMMA', 'value': ','},
                {'type': 'RCURLY', 'value': '}'},
                {'type': 'SEMICOLON', 'value': ';'},
            ]
        )

    def test_lexer_can_lex_function(self):
        """
        Test that the lexer can lex function.
        """
        self.run_test(
            input='''
            fn addFortyTwo(x: anytype) @TypeOf(x) {
                return x + 42;
            }
            ''',
            expected=[

                {'type': 'FUNCTION', 'value': 'fn'},
                {'type': 'IDENT', 'value': 'addFortyTwo'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'IDENT', 'value': 'x'},
                {'type': 'COLON', 'value': ':'},
                {'type': 'TYPE_ANYTYPE', 'value': 'anytype'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'BUILTIN_FUNCTION', 'value': 'TypeOf'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'IDENT', 'value': 'x'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'RETURN', 'value': 'return'},
                {'type': 'IDENT', 'value': 'x'},
                {'type': 'PLUS', 'value': '+'},
                {'type': 'INTEGER', 'value': 42},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'RCURLY', 'value': '}'}
            ]
        )
    
    def test_lexer_can_lex_console_output(self):
        """
        Test that the lexer can lex console output.
        """
        self.run_test(
            input='''
            const std = @import("std");
            pub fn main() void {
                std.debug.print("Hello, World!\n", .{});
            }
            ''',
            expected=[

                {'type': 'CONST', 'value': 'const'},
                {'type': 'IDENT', 'value': 'std'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'BUILTIN_FUNCTION', 'value': 'import'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'STRING', 'value': '"std"'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'PUBLIC', 'value': 'pub'},
                {'type': 'FUNCTION', 'value': 'fn'},
                {'type': 'IDENT', 'value': 'main'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'TYPE_VOID', 'value': 'void'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'IDENT', 'value': 'std'},
                {'type': 'DOT', 'value': '.'},
                {'type': 'IDENT', 'value': 'debug'},
                {'type': 'DOT', 'value': '.'},
                {'type': 'IDENT', 'value': 'print'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'STRING', 'value': '"Hello, World!\n"'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'DOT', 'value': '.'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'RCURLY', 'value': '}'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'RCURLY', 'value': '}'},
            ]
        )
    
    def test_lexer_can_lex_struct(self):
        """
        Test that the lexer can lex struct.
        """
        self.run_test(
            input='''
            const Estructura = struct {
                a: i32 = 1235,
                b:i32,
                pub fn new(a: i32, b:i32) @This() {
                    return .{
                        .a = a,
                        .b = b,
                    };
                }
            };
            const s = Estructura.new(1, 2);
            ''',
            expected=[
                {'type': 'CONST', 'value': 'const'},
                {'type': 'IDENT', 'value': 'Estructura'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'STRUCT', 'value': 'struct'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'COLON', 'value': ':'},
                {'type': 'TYPE_I32', 'value': 'i32'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'INTEGER', 'value': 1235},
                {'type': 'COMMA', 'value': ','},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'COLON', 'value': ':'},
                {'type': 'TYPE_I32', 'value': 'i32'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'PUBLIC', 'value': 'pub'},
                {'type': 'FUNCTION', 'value': 'fn'},
                {'type': 'IDENT', 'value': 'new'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'COLON', 'value': ':'},
                {'type': 'TYPE_I32', 'value': 'i32'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'COLON', 'value': ':'},
                {'type': 'TYPE_I32', 'value': 'i32'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'BUILTIN_FUNCTION', 'value': 'This'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'RETURN', 'value': 'return'},
                {'type': 'DOT', 'value': '.'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'DOT', 'value': '.'},
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'DOT', 'value': '.'},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'RCURLY', 'value': '}'},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'RCURLY', 'value': '}'},
                {'type': 'RCURLY', 'value': '}'},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'CONST', 'value': 'const'},
                {'type': 'IDENT', 'value': 's'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'IDENT', 'value': 'Estructura'},
                {'type': 'DOT', 'value': '.'},
                {'type': 'IDENT', 'value': 'new'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'INTEGER', 'value': 1},
                {'type': 'COMMA', 'value': ','},
                {'type': 'INTEGER', 'value': 2},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )

    def test_lexer_can_lex_comptime_block(self):
        """
        Test that the lexer can lex comptime block.
        """
        self.run_test(
            input='''

            comptime {
                const a: i32 = 10;
                const b: i32 = 0;
                const c = a % b;
                _ = c;
            }
            ''',
            expected=[
                {'type': 'COMPTIME',   'value': 'comptime'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'CONST',   'value': 'const'},
                {'type': 'IDENT',   'value': 'a'},
                {'type': 'COLON',   'value': ':'},
                {'type': 'TYPE_I32', 'value': 'i32'},
                {'type': 'EQUAL',   'value': '='},
                {'type': 'INTEGER', 'value': 10},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'CONST',   'value': 'const'},
                {'type': 'IDENT',   'value': 'b'},
                {'type': 'COLON',   'value': ':'},
                {'type': 'TYPE_I32', 'value': 'i32'},
                {'type': 'EQUAL',   'value': '='},
                {'type': 'INTEGER', 'value': 0},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'CONST',   'value': 'const'},
                {'type': 'IDENT',   'value': 'c'},
                {'type': 'EQUAL',   'value': '='},
                {'type': 'IDENT',   'value': 'a'},
                {'type': 'MODULE',   'value': '%'},
                {'type': 'IDENT',   'value': 'b'},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'IDENT',   'value': '_'},
                {'type': 'EQUAL',   'value': '='},
                {'type': 'IDENT',   'value': 'c'},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'RCURLY', 'value': '}'}
            ]
        )

    def test_lexer_can_lex_while_expressions(self):
        """
        Test that the lexer can lex while expressions.
        """
        self.run_test(
            input='''
            while (numero1 < numero2) {
                //This is a comment.
                var name = "John Doe";
            }
            ''',
            expected=[
                {'type': 'WHILE', 'value': 'while'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'IDENT', 'value': 'numero1'},
                {'type': 'LT', 'value': '<'},
                {'type': 'IDENT', 'value': 'numero2'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'VAR',       'value': 'var'},
                {'type': 'IDENT',     'value': 'name'},
                {'type': 'EQUAL',     'value': '='},
                {'type': 'STRING',    'value': '"John Doe"'},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'RCURLY', 'value': '}'}
            ]
        )

    def test_lexer_can_lex_comment_superiorlevel(self):
        """
        Test that the lexer can lex comment superior level.
        """
        self.run_test(
            input='//! Este módulo provee información acerca de las funciones date().',
            expected= []
        )
    
    def test_lexer_can_lex_comment_multiline(self):
        """
        Test that the lexer can lex comment multiline.
        """
        self.run_test(
            input='/// Este es un comentario\n/// multilinea.',
            expected= []
        )
    
    def test_lexer_can_lex_comment_line(self):
        """
        Test that the lexer can lex comment line.
        """
        self.run_test(
            input='//Los comentarios en Zig inician con un "//" y terminan en la siguiente línea.',
            expected= []
        )


if __name__ == '__main__':
    unittest.main()
