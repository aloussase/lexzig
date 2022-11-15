import ply.yacc as yacc

from lexzig.lexer import Lexer


class Parser:
    """
    Implements a parser for a subset of the Zig programming language.
    """

    tokens = Lexer.tokens

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLICATION', 'DIVISION'),
    )

    def __init__(self):
        self.parser = yacc.yacc(module=self)

    def p_program(self, p):
        '''
        program : stmt stmts

        stmts : stmt stmts
              | empty
        '''

    def p_stmt(self, p):
        '''
        stmt : assignment_stmt
             | functiondecl_stmt
        '''

    def p_assignment_stmt(self, p):
        '''
        assignment_stmt : vardecl IDENT assignment_stmt_tail
                        | vardecl IDENT COLON typedecl assignment_stmt_tail

        assignment_stmt_tail : EQUAL expression SEMICOLON
        '''

    # TODO: Error union type in return type.
    def p_functiondecl_stmt(self, p):
        '''
        functiondecl_stmt : function_signature function_body

        param : IDENT colon_type

        params_list : param
                    | param COMMA params_list
                    | empty

        function_signature : access_modifier FUNCTION IDENT LPAREN params_list RPAREN typedecl

        function_body : LCURLY stmts RCURLY
        '''

    def p_colon_type(self, p):
        '''
        colon_type : COLON typedecl
                   | empty
        '''

    def p_access_modifier(self, p):
        '''
        access_modifier : PUB
                        | empty
        '''

    def p_vardecl(self, p):
        '''
        vardecl : VAR
                | CONST
                | COMPTIME
        '''

    # TODO: Arrays
    def p_typedecl(self, p):
        '''
        typedecl : TYPE_I32
                 | TYPE_I8
                 | TYPE_U8
                 | TYPE_I16
                 | TYPE_U16
                 | TYPE_U32
                 | TYPE_I64
                 | TYPE_U64
                 | TYPE_I128
                 | TYPE_U128
                 | TYPE_ISIZE
                 | TYPE_USIZE
                 | TYPE_C_SHORT
                 | TYPE_C_USHORT
                 | TYPE_C_INT
                 | TYPE_C_UINT
                 | TYPE_C_LONG
                 | TYPE_C_ULONG
                 | TYPE_C_LONGLONG
                 | TYPE_C_ULONGLONG
                 | TYPE_C_LONGDOUBLE
                 | TYPE_F16
                 | TYPE_F32
                 | TYPE_F64
                 | TYPE_F80
                 | TYPE_F128
                 | TYPE_BOOL
                 | TYPE_ANYOPAQUE
                 | TYPE_VOID
                 | TYPE_NORETURN
                 | TYPE_TYPE
                 | TYPE_ANYERROR
                 | TYPE_ANYTYPE
                 | TYPE_COMPTIME_INT
                 | TYPE_COMPTIME_FLOAT
                 | TYPE_NULL
                 | TYPE_UNDEFINED
        '''

    def p_expression(self, p):
        '''
        expression : INTEGER PLUS INTEGER
                   | INTEGER MINUS INTEGER
                   | INTEGER MULTIPLICATION INTEGER
                   | INTEGER DIVISION INTEGER
                   | INTEGER
        '''
        if len(p) == 2:
            p[0] = p[1]
            return

        op = p[2]
        lhs = p[1]
        rhs = p[3]

        if op == '+':
            p[0] = lhs + rhs
        elif op == '-':
            p[0] = lhs - rhs
        elif op == '*':
            p[0] = lhs * rhs
        elif op == '/':
            p[0] = lhs / rhs

    def p_empty(self, _) -> None:
        'empty :'

    def parse(self, input: str):
        return self.parser.parse(input, lexer=Lexer().lexer)
