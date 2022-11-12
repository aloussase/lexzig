import ply.lex as pylex


class Lexer:
    """
    Implements a lexer for a subset of the Zig programming language.
    """

    types = [
        'i8', 'u8', 'i16', 'u16', 'i32', 'u32', 'i64', 'u64', 'i128', 'u128', 'isize', 'usize',
        'c_short', 'c_ushort', 'c_int', 'c_uint', 'c_long', 'c_ulong', 'c_longlong', 'c_ulonglong',
        'c_longdouble', 'f16', 'f32', 'f64', 'f80', 'f128', 'bool', 'anyopaque', 'void', 'noreturn',
        'type', 'anyerror', 'comptime_int', 'comptime_float', 'null', 'undefined'
    ]

    keywords = {
        'const': 'CONST',
        'var': 'VAR',
        'if': 'IF',
        'else': 'ELSE',
        'return': 'RETURN',
        'test': 'TEST',
        'extern': 'EXTERN',
        'export': 'EXPORT',
        'threadlocal': 'THREADLOCAL',
        'comptime': 'COMPTIME',
        **{t: f'TYPE_{t.upper()}' for t in types},
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
        r'(@"[^"]*"|[a-zA-Z_][a-zA-Z_0-9]*)'

        # Check to see if the identifier is actually a keyword.
        t.type = self.keywords.get(t.value, 'IDENT')

        # Remove the @"" from special variable names.
        if t.value.startswith('@'):
            t.value = t.value[2:-1]

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
