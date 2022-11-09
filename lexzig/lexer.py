import ply.lex as pylex

class Lexer:
    """
    Implements a lexer for a subset of the Zig programming language.
    """

    keywords = {
        'const': 'CONST',
        'var': 'VAR',
        'undefined': 'UNDEFINED',
        'u8': 'TYPE_U8',
    }

    tokens = [
        'IDENT',
        'STRING',
        'LBRACE',
        'RBRACE',
        'INTEGER',
        'EQUAL',
        'SEMICOLON',
        'COLON',
    ] + list(keywords.values())

    t_LBRACE = r'\['
    t_RBRACE = r'\]'
    t_EQUAL = r'='
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_STRING = r'"[^"]*"'

    t_ignore = r' '

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.keywords.get(t.value, 'IDENT')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self, **kwargs):
        self.lexer = pylex.lex(module=self, **kwargs)

    def lex(self, input: str):
        self.lexer.input(input)
        return list(self.lexer)
