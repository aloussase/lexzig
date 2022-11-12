from ply.lex import LexToken  # type: ignore
import unittest
from typing import List, Dict, Literal, Any, TypedDict

from lexzig.lexer import Lexer

TestCase = TypedDict('TestCase', type=str, value=Any)


class TestLexer(unittest.TestCase):
    lexer = Lexer()

    def run_test(self, *, input: str, expected: List[TestCase]):
        tokens: List[LexToken] = self.lexer.lex(input)

        self.assertEqual(len(expected), len(tokens))

        for test, actual in zip(expected, tokens):
            self.assertEqual(test['type'], actual.type)  # type: ignore
            self.assertEqual(test['value'], actual.value)  # type: ignore

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

    def test_lexer_can_lex_enums(self):
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

    def test_lexer_can_lex_the_input_example(self):
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
            ]
        )


if __name__ == '__main__':
    unittest.main()
