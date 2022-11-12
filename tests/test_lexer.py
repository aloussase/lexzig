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


if __name__ == '__main__':
    unittest.main()
