import ply.lex as pylex  # type: ignore
from ply.lex import LexToken
from typing import List, Dict, Any


class Lexer:
    """
    Implements a lexer for a subset of the Zig programming language.
    """

    types: List[str] = [
        'i8', 'u8', 'i16', 'u16', 'i32', 'u32', 'i64', 'u64', 'i128', 'u128', 'isize', 'usize',
        'c_short', 'c_ushort', 'c_int', 'c_uint', 'c_long', 'c_ulong', 'c_longlong', 'c_ulonglong',
        'c_longdouble', 'f16', 'f32', 'f64', 'f80', 'f128', 'bool', 'anyopaque', 'void', 'noreturn',
        'type', 'anyerror', 'comptime_int', 'comptime_float', 'null', 'undefined'
    ]

    keywords: Dict[str, str] = {
        'comptime': 'COMPTIME',
        'const': 'CONST',
        'else': 'ELSE',
        'export': 'EXPORT',
        'extern': 'EXTERN',
        'enum': 'ENUM',
        'fn': 'FUNCTION',
        'if': 'IF',
        'return': 'RETURN',
        'switch': 'SWITCH',
        'test': 'TEST',
        'threadlocal': 'THREADLOCAL',
        'try': 'TRY',
        'pub': 'PUB',
        'var': 'VAR',
        **{t: f'TYPE_{t.upper()}' for t in types},
    }

    tokens: List[str] = [
        'UNDERSCORE',
        'AMPERSAND',
        'BANG',
        'BUILTIN_FUNCTION',
        'COLON',
        'COMMA',
        'CHAR',
        'DOT',
        'EQUAL',
        'ELLIPSIS',
        'FAT_ARROW',
        'IDENT',
        'INTEGER',
        'LBRACE',
        'LCURLY',
        'LPAREN',
        'LT',
        'RBRACE',
        'RCURLY',
        'RPAREN',
        'SEMICOLON',
        'STRING',
    ] + list(keywords.values())

    t_AMPERSAND = r'&'
    t_BANG = r'!'
    t_COLON = r':'
    t_COMMA = r','
    t_CHAR = r"'[^']'"
    t_DOT = '\.'
    t_FAT_ARROW = r'=>'
    t_ELLIPSIS = r'\.\.\.'
    t_EQUAL = r'='
    t_LBRACE = r'\['
    t_LCURLY = r'{'
    t_LPAREN = r'\('
    t_LT = r'<'
    t_RBRACE = r'\]'
    t_RCURLY = r'}'
    t_RPAREN = r'\)'
    t_SEMICOLON = r';'
    t_STRING = r'"[^"]*"'

    t_ignore = ' \t'

    def t_BUILTIN_FUNCTION(self, t: LexToken) -> LexToken:
        r'@[a-zA-Z_][a-zA-Z_0-9]*'
        t.value = t.value[1:]
        return t

    def t_INTEGER(self, t: LexToken) -> LexToken:
        r'\d+'
        t.value = int(t.value)
        return t

    def t_IDENT(self, t: LexToken) -> LexToken:
        r'(@"[^"]*"|[a-zA-Z_][a-zA-Z_0-9]*)'

        # Check to see if the identifier is actually a keyword.
        t.type = self.keywords.get(t.value, 'IDENT')

        # Remove the @"" from special variable names.
        if t.value.startswith('@'):
            t.value = t.value[2:-1]

        if t.value == '_':
            t.type = 'UNDERSCORE'

        return t

    def t_newline(self, t: LexToken) -> None:
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t: LexToken) -> None:
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        self.lexer = pylex.lex(module=self, **kwargs)

    def lex(self, input: str) -> List[LexToken]:
        self.lexer.input(input)
        return list(self.lexer)
