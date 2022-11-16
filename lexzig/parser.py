import ply.yacc as yacc

from lexzig.lexer import Lexer
import lexzig.ast as ast


class Parser:
    """
    Implements a parser for a subset of the Zig programming language.
    """

    tokens = Lexer.tokens

    precedence = (
        ('nonassoc', 'LT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLICATION', 'DIVISION'),
    )

    def __init__(self):
        self.parser = yacc.yacc(module=self)

    def p_program(self, p):
        '''
        program : stmts
        '''
        p[0] = ast.Program(stmts=p[1])

    def p_stmts(self, p):
        '''
        stmts : stmt stmts
              | empty
        '''
        if len(p) == 3:
            p[0] = p[2]
            if not p[0]:
                p[0] = []
            p[0].insert(0, p[1])

    def p_stmt(self, p):
        '''
        stmt : assignment_stmt
             | functiondecl_stmt
             | expression_stmt
        '''
        p[0] = p[1]

    def p_assignment_stmt(self, p):
        '''
        assignment_stmt : vardecl IDENT assignment_stmt_tail
                        | vardecl IDENT COLON compound_typedecl assignment_stmt_tail
                        | UNDERSCORE assignment_stmt_tail
        '''
        p[0] = ast.AssignmentStmt(
            ident=ast.Identifier(p[2] if len(p) > 3 else p[1]),
            value=p[len(p) - 1]
        )

    def p_assignment_stmt_tail(self, p):
        '''
        assignment_stmt_tail : EQUAL expression SEMICOLON
        '''
        p[0] = p[2]

    def p_functiondecl_stmt(self, p):
        '''
        functiondecl_stmt : function_signature function_body
        '''
        name, params = p[1]
        stmts = p[2]
        p[0] = ast.FunctionDeclStmt(
            name=ast.Identifier(name),
            params=params,
            body=stmts
        )

    # TODO: Error union type in return type.
    def p_function_param(self, p):
        'function_param : IDENT colon_type'
        p[0] = ast.Identifier(p[1])

    def p_function_param_list(self, p):
        '''
        function_param_list : function_param
                    | function_param COMMA function_param_list
                    | empty
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = p[len(p) - 1]
            p[0].insert(0, p[1])

    def p_function_signature(self, p):
        '''
        function_signature : access_modifier FUNCTION IDENT LPAREN function_param_list RPAREN compound_typedecl
        '''
        name = p[3]
        params = p[5] if p[5] else []
        p[0] = (name, params)

    def p_function_body(self, p):
        '''
        function_body : LCURLY stmts RCURLY
        '''
        p[0] = p[2] if p[2] else []

    def p_colon_type(self, p):
        '''
        colon_type : COLON compound_typedecl
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

    def p_compound_typedecl(self, p):
        '''
        compound_typedecl : LBRACE RBRACE typedecl
                          | LBRACE INTEGER RBRACE typedecl
                          | typedecl
        '''

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

    def p_expression_stmt(self, p) -> None:
        '''
        expression_stmt : expression SEMICOLON
        '''
        p[0] = p[1]

    def p_expression(self, p) -> None:
        '''
        expression : arithmetic_expression
                   | comparison_expression
                   | if_expression
                   | value_expression
        '''
        p[0] = p[1]

    def p_value_expression(self, p) -> None:
        '''
        value_expression : INTEGER
                         | STRING
                         | IDENT
                         | CHAR
        '''
        # TODO: It would be better to check the token type.
        # TODO: Test this.
        if isinstance(p[1], int):
            p[0] = ast.Integer(p[1])
        elif isinstance(p[1], str):
            if p[1][0] == "'":
                p[0] = ast.Char(p[1])
            elif p[1][0] == '"':
                p[0] = ast.String(p[1])
            else:
                p[0] = ast.Identifier(p[1])

    def p_arithmetic_expression(self, p) -> None:
        '''
        arithmetic_expression : INTEGER PLUS INTEGER
                              | INTEGER MINUS INTEGER
                              | INTEGER MULTIPLICATION INTEGER
                              | INTEGER DIVISION INTEGER
        '''
        lhs, op, rhs = p[1:4]

        if op == '+':
            p[0] = ast.BinOp(lhs=lhs, op='+', rhs=rhs)
        elif op == '-':
            p[0] = ast.BinOp(lhs=lhs, op='-', rhs=rhs)
        elif op == '*':
            p[0] = ast.BinOp(lhs=lhs, op='*', rhs=rhs)
        elif op == '/':
            p[0] = ast.BinOp(lhs=lhs, op='/', rhs=rhs)

    def p_comparison_expression(self, p) -> None:
        '''
        comparison_expression : expression LT expression
        '''
        p[0] = ast.BinOp(lhs=p[1], op=p[2], rhs=p[3])

    def p_if_expression(self, p):
        '''
        if_expression : IF LPAREN expression RPAREN expression ELSE expression
        '''
        p[0] = ast.IfExpr(condition=p[3], ifBranch=p[5], elseBranch=p[7])

    def p_empty(self, _) -> None:
        'empty :'

    def p_error(self, p) -> None:
        '''
        Skip tokens until we meet a synchronization point, a semicolon in this
        case.
        '''
        if not p:
            print('Unexpected end of file while parsing')
            return

        while True:
            token = self.parser.token()
            if not token or token.type == 'SEMICOLON':
                break

        self.parser.restart()

    def parse(self, input: str):
        return self.parser.parse(input, lexer=Lexer().lexer)
