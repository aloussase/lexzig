from ply.lex import LexToken  # type: ignore
import unittest
from typing import List, Dict, Literal, Any, TypedDict

from lexzig.lexer import Lexer

TestCase = TypedDict('TestCase', {'type': str, 'value': Any})


class TestLexer(unittest.TestCase):
    lexer = Lexer()

    def run_test(self, *, input: str, expected: List[TestCase]) -> None:
        tokens: List[LexToken] = self.lexer.lex(input)

        self.assertEqual(len(expected), len(tokens))

        for test, actual in zip(expected, tokens):
            self.assertEqual(test['type'], actual.type)  # type: ignore
            self.assertEqual(test['value'], actual.value)  # type: ignore

    def test_lexer_can_lex_special_variable_names(self) -> None:
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

    def test_lexer_can_lex_builtin_functions(self) -> None:
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

    def test_lexer_can_lex_const_variable_declarations(self) -> None:
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

    def test_lexer_can_lex_variable_declarations(self) -> None:
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

    def test_lexer_can_lex_if_expressions(self) -> None:
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

    def test_lexer_can_lex_switch_expressions(self) -> None:
        """
        Test that the lexer can lex switch expressions.
        """
        self.run_test(
            input='''
            var x = switch (10) {
                0...1 => 20,
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
                {'type': 'INTEGER', 'value': 0},
                {'type': 'ELLIPSIS', 'value': '...'},
                {'type': 'INTEGER', 'value': 1},
                {'type': 'FAT_ARROW', 'value': '=>'},
                {'type': 'INTEGER', 'value': 20},
                {'type': 'COMMA', 'value': ','},
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
    def test_lexer_can_lex_for_expressions(self) -> None:
        """
        Test that the lexer can lex for expressions.
        """
        self.run_test(
            input='''
            for(items) |value| {
                sum=+value;
            }
            ''',
            expected=[
                {'type': 'FOR', 'value': 'for'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'IDENT', 'value': 'items'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'BAR', 'bar': '|'},
                {'type': 'IDENT', 'value': 'value'},
                {'type': 'BAR', 'bar': '|'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'IDENT', 'value': 'sum'},
                {'type': 'PLUS_EQUAL', 'value': '+='},
                {'type': 'IDENT', 'value': 'value'},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'RCURLY', 'value': '}'}
            ]
        )

    def test_lexer_can_lex_enums(self) -> None:
        """
        Test that the lexer can lex enums.
        """
        self.run_test(
            input=r'const Direction = enum { north, south, east, west };',
            expected=[
                {'type': 'CONST', 'value': 'const'},
                {'type': 'IDENT', 'value': 'Direction'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'ENUM', 'value': 'enum'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'IDENT', 'value': 'north'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'IDENT', 'value': 'south'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'IDENT', 'value': 'east'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'IDENT', 'value': 'west'},
                {'type': 'RCURLY', 'value': '}'},
                {'type': 'SEMICOLON', 'value': ';'},
            ]
        )
    
    def test_lexer_can_lex_short_addition_expressions(self) -> None:
        """
        Test that the lexer can lex short addition expressions.
        """
        self.run_test(
            input='''
            a += b;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'PLUS_EQUAL', 'value': '+='},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'SEMICOLON', 'value': ';'}       
            ]
        )

    def test_lexer_can_lex_addition_expressions(self) -> None:
        """
        Test that the lexer can lex addition expressions.
        """
        self.run_test(
            input='''
            a = 1 + 2;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'INTEGER', 'value': '1'},
                {'type': 'PLUS', 'value': '+'},
                {'type': 'INTEGER', 'value': '2'},
                {'type': 'SEMICOLON', 'value': ';'}        
            ]
        )

    def test_lexer_can_lex_short_subtraction_expressions(self) -> None:
        """
        Test that the lexer can lex short subtraction expressions.
        """
        self.run_test(
            input='''
            a -= b;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'MINUS_EQUAL', 'value': '-='},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )
    def test_lexer_can_lex_subtraction_expressions(self) -> None:
        """
        Test that the lexer can lex subtraction expressions.
        """
        self.run_test(
            input='''
            a = 3 - 2;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'INTEGER', 'value': '3'},
                {'type': 'MINUS', 'value': '-'},
                {'type': 'INTEGER', 'value': '2'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        ) 

    def test_lexer_can_lex_short_multiplication_expressions(self) -> None:
        """
        Test that the lexer can lex short multiplication expressions.
        """
        self.run_test(
            input='''
            a *= b;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'MULT_EQUAL', 'value': '*='},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )
    def test_lexer_can_lex_multiplication_expressions(self) -> None:
        """
        Test that the lexer can lex multiplication expressions.
        """
        self.run_test(
            input='''
            a = 3 * 2;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'INTEGER', 'value': '3'},
                {'type': 'MULTIPLICATION', 'value': '*'},
                {'type': 'INTEGER', 'value': '2'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )
    def test_lexer_can_lex_short_division_expressions(self) -> None:
        """
        Test that the lexer can lex short division expressions.
        """
        self.run_test(
            input='''
            a /= b;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'DIV_EQUAL', 'value': '/='},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )

    def test_lexer_can_lex_division_expressions(self) -> None:
        """
        Test that the lexer can lex division expressions.
        """
        self.run_test(
            input='''
            a = 4 / 2;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'INTEGER', 'value': '4'},
                {'type': 'DIVISION', 'value': '/'},
                {'type': 'INTEGER', 'value': '2'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )
    def test_lexer_can_lex_short_module_expressions(self) -> None:
        """
        Test that the lexer can lex short module expressions.
        """
        self.run_test(
            input='''
            a %= b;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'MOD_EQUAL', 'value': '%='},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )
    def test_lexer_can_lex_module_expressions(self) -> None:
        """
        Test that the lexer can lex module expressions.
        """
        self.run_test(
            input='''
            a = 4 % 2;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'INTEGER', 'value': '4'},
                {'type': 'MODULE', 'value': '%'},
                {'type': 'INTEGER', 'value': '2'},
                {'type': 'SEMICOLON', 'value': ';'}        
            ]
        ) 
        
    def test_lexer_can_lex_the_input_example(self) -> None:
        """
        Test that the lexer can lex the input example.
        """
        self.run_test(
            input="""
                const std = @import("std");

                pub fn main() !void {
                    const stdin = std.io.getStdIn().reader();
                    var buf: [100]u8 = undefined;
                    const line = try stdin.readUntilDelimiter(&buf, '\n');
                    _ = line;
                }
            """,
            expected=[
                # const std = @import("std");
                {'type': 'CONST', 'value': 'const'},
                {'type': 'IDENT', 'value': 'std'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'BUILTIN_FUNCTION', 'value': 'import'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'STRING', 'value': '"std"'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'SEMICOLON', 'value': ';'},
                # pub fn main() !void {
                {'type': 'PUB', 'value': 'pub'},
                {'type': 'FUNCTION', 'value': 'fn'},
                {'type': 'IDENT', 'value': 'main'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'BANG', 'value': '!'},
                {'type': 'TYPE_VOID', 'value': 'void'},
                {'type': 'LCURLY', 'value': '{'},
                # const stdin = std.io.getStdIn().reader();
                {'type': 'CONST', 'value': 'const'},
                {'type': 'IDENT', 'value': 'stdin'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'IDENT', 'value': 'std'},
                {'type': 'DOT', 'value': '.'},
                {'type': 'IDENT', 'value': 'io'},
                {'type': 'DOT', 'value': '.'},
                {'type': 'IDENT', 'value': 'getStdIn'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'DOT', 'value': '.'},
                {'type': 'IDENT', 'value': 'reader'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'SEMICOLON', 'value': ';'},
                # var buf: [100]u8 = undefined;
                {'type': 'VAR', 'value': 'var'},
                {'type': 'IDENT', 'value': 'buf'},
                {'type': 'COLON', 'value': ':'},
                {'type': 'LBRACE', 'value': '['},
                {'type': 'INTEGER', 'value': 100},
                {'type': 'RBRACE', 'value': ']'},
                {'type': 'TYPE_U8', 'value': 'u8'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'TYPE_UNDEFINED', 'value': 'undefined'},
                {'type': 'SEMICOLON', 'value': ';'},
                # const line = try stdin.readUntilDelimiter(&buf, ’\n’);
                {'type': 'CONST', 'value': 'const'},
                {'type': 'IDENT', 'value': 'line'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'TRY', 'value': 'try'},
                {'type': 'IDENT', 'value': 'stdin'},
                {'type': 'DOT', 'value': '.'},
                {'type': 'IDENT', 'value': 'readUntilDelimiter'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'AMPERSAND', 'value': '&'},
                {'type': 'IDENT', 'value': 'buf'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'CHAR', 'value': '\'\n\''},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'SEMICOLON', 'value': ';'},
                # _ = line;
                {'type': 'UNDERSCORE', 'value': '_'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'IDENT', 'value': 'line'},
                {'type': 'SEMICOLON', 'value': ';'},
                # }
                {'type': 'RCURLY', 'value': '}'},
            ])

    def test_lexer_can_lex_function(self) -> None:
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

    def test_lexer_can_lex_console_output(self) -> None:
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
                {'type': 'PUB', 'value': 'pub'},
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
    def test_lexer_can_lex_array_expressions(self) -> None:
        """
        Test that the lexer can lex array expressions.
        """
        self.run_test(
            input='''
            const items = [_]i32 { 4, 5, 3 };
            ''',
            expected=[
                {'type': 'CONST', 'value': 'const'},
                {'type': 'IDENT', 'value': 'items'},
                {'type': 'EQUAL', 'value': '='},
                {'type': 'LBRACE', 'value': '['},
                {'type': 'UNDERSCORE', 'value': '_'},
                {'type': 'RBRACE', 'value': ']'},
                {'type': 'TYPE_I32', 'value': 'i32'},
                {'type': 'LCURLY', 'value': '{'},
                {'type': 'INTEGER', 'value': '4'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'INTEGER', 'value': '5'},
                {'type': 'COMMA', 'value': ','},
                {'type': 'INTEGER', 'value': '3'},                
                {'type': 'RCURLY', 'value': '}'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )

    def test_lexer_can_lex_struct(self) -> None:
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
                {'type': 'PUB', 'value': 'pub'},
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

    def test_lexer_can_lex_comptime_block(self) -> None:
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
                {'type': 'UNDERSCORE',   'value': '_'},
                {'type': 'EQUAL',   'value': '='},
                {'type': 'IDENT',   'value': 'c'},
                {'type': 'SEMICOLON', 'value': ';'},
                {'type': 'RCURLY', 'value': '}'}
            ]
        )

    def test_lexer_can_lex_while_expressions(self) -> None:
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

    def test_lexer_can_lex_comment_superiorlevel(self) -> None:
        """
        Test that the lexer can lex comment superior level.
        """
        self.run_test(
            input='//! Este módulo provee información acerca de las funciones date().',
            expected=[]
        )

    def test_lexer_can_lex_comment_multiline(self) -> None:
        """
        Test that the lexer can lex comment multiline.
        """
        self.run_test(
            input='/// Este es un comentario\n/// multilinea.',
            expected=[]
        )

    def test_lexer_can_lex_comment_line(self) -> None:
        """
        Test that the lexer can lex comment line.
        """
        self.run_test(
            input='//Los comentarios en Zig inician con un "//" y terminan en la siguiente línea.',
            expected=[]
        )
    def test_lexer_can_lex_equal_expressions(self) -> None:
        """
        Test that the lexer can lex equal expressions.
        """
        self.run_test(
            input='''
            a == b;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'IS_EQUAL_TO', 'value': '=='},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        ) 
    def test_lexer_can_lex_different_expressions(self) -> None:
        """
        Test that the lexer can lex different expressions.
        """
        self.run_test(
            input='''
            a != b;
            ''',
            expected=[
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'IS_NOT_EQUAL', 'value': '!='},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )
    def test_lexer_can_lex_not_expressions(self) -> None:
        """
        Test that the lexer can lex not expressions.
        """
        self.run_test(
            input='''
            !(a == b);
            ''',
            expected=[
                {'type': 'BANG', 'value': '!'},
                {'type': 'LPAREN', 'value': '('},
                {'type': 'IDENT', 'value': 'a'},
                {'type': 'IS_EQUAL_TO', 'value': '=='},
                {'type': 'IDENT', 'value': 'b'},
                {'type': 'RPAREN', 'value': ')'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )
    def test_lexer_can_lex_greater_than_expressions(self) -> None:
        """
        Test that the lexer can lex greater than expressions.
        """
        self.run_test(
            input='''
            1 > 0;
            ''',
            expected=[
                {'type': 'INTEGER', 'value': '1'},
                {'type': 'GREATER_THAN', 'value': '>'},
                {'type': 'INTEGER', 'value': '0'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )
    def test_lexer_can_lex_less_than_expressions(self) -> None:
        """
        Test that the lexer can lex less than expressions.
        """
        self.run_test(
            input='''
            2 < 5;
            ''',
            expected=[
                {'type': 'INTEGER', 'value': '2'},
                {'type': 'LESS_THAN', 'value': '<'},
                {'type': 'INTEGER', 'value': '5'},
                {'type': 'SEMICOLON', 'value': ';'}
            ]
        )
             

if __name__ == '__main__':
    unittest.main()
