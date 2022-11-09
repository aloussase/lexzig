import unittest

from lexzig.lexer import Lexer


class TestLexer(unittest.TestCase):
    lexer = Lexer()

    def run_test(self, *, input: str, expected):
        tokens = self.lexer.lex(input)
        tests = expected
        self.assertEqual(len(tests), len(tokens))
        for expected, actual in zip(tests, tokens):
            self.assertEqual(expected['type'], actual.type)
            self.assertEqual(expected['value'], actual.value)

    def test_lexer_can_lex_const_variable_declarations(self):
        """
        Test that the lexer can lex constant variable declarations.
        """
        self.run_test(
            input = r"const buffer: [100]u8 = undefined;",
            expected =  [
                { 'type': 'CONST',   'value': 'const' },
                { 'type': 'IDENT',   'value': 'buffer' },
                { 'type': 'COLON',   'value': ':' },
                { 'type': 'LBRACE',  'value': '[' },
                { 'type': 'INTEGER', 'value': 100 },
                { 'type': 'RBRACE',  'value': ']' },
                { 'type': 'TYPE_U8', 'value': 'u8' },
                { 'type': 'EQUAL',   'value': '=' },
                { 'type': 'UNDEFINED', 'value': 'undefined' },
                { 'type': 'SEMICOLON', 'value': ';' },
            ]
        )

    def test_lexer_can_lex_variable_declarations(self):
        """
        Test that the lexer can lex variable declarations.
        """
        self.run_test(
            input = r'var name = "John Doe";',
            expected =  [
                { 'type': 'VAR',       'value': 'var' },
                { 'type': 'IDENT',     'value': 'name' },
                { 'type': 'EQUAL',     'value': '=' },
                { 'type': 'STRING',    'value': '"John Doe"' },
                { 'type': 'SEMICOLON', 'value': ';' },
            ]
        )


if __name__ == '__main__':
    unittest.main()
