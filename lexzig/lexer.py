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
        'bool': 'TYPE_BOOL',
        'if': 'IF',
        'else': 'ELSE',
        'return': 'RETURN',
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
        'LPAREN',
        'RPAREN',
        'LCURLY',
        'RCURLY',
        'LT',
        'BUILTIN_FUNCTION'
    ] + list(keywords.values())

    t_LBRACE = r'\['
    t_RBRACE = r'\]'
    t_EQUAL = r'='
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_STRING = r'"[^"]*"'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LCURLY = r'{'
    t_RCURLY = r'}'
    t_LT = r'<'
    t_BUILTIN_FUNCTION = r'@[a-zA-Z_][a-zA-Z_0-9]*'

    t_ignore = r' \t'

    def t_INTEGER(self, t: pylex.LexToken):
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
