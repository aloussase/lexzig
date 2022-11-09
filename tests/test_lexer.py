import unittest

from lexzig.lexer import Lexer


class TestLexer(unittest.TestCase):
    def test_lexer_can_lex_const_variable_declarations(self):
        """
        Test that the lexer can lex variable declarations.
        """
        # Arrange
        lexer = Lexer()
        input = r"const buffer: [100]u8 = undefined;"
        tests = [
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

        # Act
        tokens = lexer.lex(input)

        # Assert
        self.assertEqual(len(tokens), 10)

        for expected, actual in zip(tests, tokens):
            self.assertEqual(expected['type'], actual.type)
            self.assertEqual(expected['value'], actual.value)


if __name__ == '__main__':
    unittest.main()
