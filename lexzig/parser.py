from typing import cast

from ply.lex import LexToken  # type: ignore
import ply.yacc as yacc  # type: ignore
from ply.yacc import YaccProduction

import lexzig.ast as ast
from lexzig.lexer import Lexer


class ParserError(Exception):
    def __init__(self, message: str, lineno: int):
        super().__init__(message)
        self.message = message
        self.lineno = lineno


class Parser:
    """
    Implements a parser for a subset of the Zig programming language.
    """

    tokens = Lexer.tokens

    precedence = (
        # Make else bind weaker than other operators to avoid conflicts
        # with if expressions.
        ('left', 'ELSE'),
        ('nonassoc', 'MINUS_EQUAL', 'MOD_EQUAL',
         'MULT_EQUAL', 'PLUS_EQUAL', 'DIV_EQUAL', 'EQUAL'),
        ('nonassoc', 'LT', 'IS_EQUAL_TO', 'GREATER_THAN', 'IS_NOT_EQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLICATION', 'DIVISION', 'MODULE'),
        ('right', 'AMPERSAND'),
        ('left', 'DOT'),
    )

    def __init__(self) -> None:
        self.parser = yacc.yacc(module=self, debug=True)

    def p_program(self, p: YaccProduction) -> None:
        """
        program : stmts
        """
        p[0] = ast.Program(stmts=p[1])

    def p_stmts(self, p: YaccProduction) -> None:
        """
        stmts : stmt stmts
              | empty
        """
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = []

    def p_stmt(self, p: YaccProduction) -> None:
        """
        stmt : assignment_stmt
             | functiondecl_stmt
             | expression_stmt
             | return_stmt
             | for_stmt
             | while_stmt
        """
        p[0] = p[1]

    def p_return_stmt(self, p: YaccProduction) -> None:
        """
        return_stmt : RETURN expression SEMICOLON
        """
        p[0] = ast.ReturnStmt(p[2])

    def p_assignment_expression(self, p: YaccProduction) -> None:
        """
        assignment_expression : IDENT assignment_stmt_tail
        """
        op, value = p[2]
        p[0] = ast.AssignmentExpr(
            ident=ast.Identifier(p[1]),
            op=op,
            value=value
        )

    def p_assignment_stmt(self, p: YaccProduction) -> None:
        """
        assignment_stmt : vardecl IDENT assignment_stmt_tail SEMICOLON
                        | vardecl IDENT COLON error_union_typedecl assignment_stmt_tail SEMICOLON
                        | UNDERSCORE assignment_stmt_tail SEMICOLON
        """
        _, value = p[len(p) - 2]
        p[0] = ast.AssignmentStmt(
            ident=ast.Identifier(p[2] if len(p) > 4 else p[1]),
            value=value
        )

    def p_assignment_stmt_tail(self, p: YaccProduction) -> None:
        """
        assignment_stmt_tail : EQUAL expression
                             | MINUS_EQUAL expression
                             | MOD_EQUAL expression
                             | MULT_EQUAL expression
                             | PLUS_EQUAL expression
                             | DIV_EQUAL expression
        """
        p[0] = (p[1], p[2])

    def p_functiondecl_stmt(self, p: YaccProduction) -> None:
        """
        functiondecl_stmt : function_signature function_body
        """
        name, params = p[1]
        stmts = p[2]
        p[0] = ast.FunctionDeclStmt(
            name=ast.Identifier(name),
            params=params,
            body=stmts
        )

    def p_function_param(self, p: YaccProduction) -> None:
        """function_param : IDENT COLON compound_typedecl"""
        p[0] = ast.Identifier(p[1])

    def p_function_param_list(self, p: YaccProduction) -> None:
        """
        function_param_list : function_param_list function_param COMMA
                            | function_param_list function_param
                            | empty
        """
        if 3 <= len(p) <= 4:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = []

    def p_function_signature(self, p: YaccProduction) -> None:
        """
        function_signature : PUB EXPORT FUNCTION IDENT LPAREN function_param_list RPAREN error_union_typedecl
                           | PUB FUNCTION IDENT LPAREN function_param_list RPAREN error_union_typedecl
                           | EXPORT FUNCTION IDENT LPAREN function_param_list RPAREN error_union_typedecl
                           | FUNCTION IDENT LPAREN function_param_list RPAREN error_union_typedecl
        """
        if len(p) == 9:
            p[0] = (p[4], p[6])
        elif len(p) == 8:
            p[0] = (p[3], p[5])
        else:
            p[0] = (p[2], p[4])

    def p_function_body(self, p: YaccProduction) -> None:
        """
        function_body : LCURLY stmts RCURLY
        """
        p[0] = p[2]

    def p_vardecl(self, p: YaccProduction) -> None:
        """
        vardecl : EXPORT vardecl_tail
                | vardecl_tail
        """

    def p_vardecl_tail(self, p: YaccProduction) -> None:
        """
        vardecl_tail : VAR
                     | CONST
                     | COMPTIME
        """

    def p_compound_typedecl(self, p: YaccProduction) -> None:
        """
        compound_typedecl : LBRACE RBRACE typedecl
                          | LBRACE INTEGER RBRACE typedecl
                          | LBRACE UNDERSCORE RBRACE typedecl
                          | typedecl
        """

    def p_error_union_typedecl(self, p: YaccProduction) -> None:
        """
        error_union_typedecl : BANG compound_typedecl
                             | IDENT BANG compound_typedecl
                             | compound_typedecl
        """

    def p_typedecl(self, p: YaccProduction) -> None:
        """
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
                 | IDENT
        """

    def p_expression_stmt(self, p: YaccProduction) -> None:
        """
        expression_stmt : expression SEMICOLON
        """
        p[0] = p[1]

    def p_expression(self, p: YaccProduction) -> None:
        """
        expression : postfix_expression
        """
        p[0] = p[1]

    def p_postfix_expression(self, p: YaccProduction) -> None:
        """
        postfix_expression : field_access
                           | function_call
                           | primary_expression
        """
        p[0] = p[1]

    def p_primary_expresssion(self, p: YaccProduction) -> None:
        """
        primary_expression : arithmetic_expression
                           | comparison_expression
                           | if_expression
                           | switch_expression
                           | struct_decl
                           | enum_decl
                           | anon_array
                           | struct_instantiation
                           | try_expression
                           | unary_expression
                           | assignment_expression
                           | value_expression
        """
        p[0] = p[1]

    def p_unary_expression(self, p: YaccProduction) -> None:
        """
        unary_expression : AMPERSAND expression
        """
        p[0] = ast.UnaryOp(op=p[1], rhs=p[2])

    def p_value_expression(self, p: YaccProduction) -> None:
        """
        value_expression : INTEGER
                         | STRING
                         | IDENT
                         | CHAR
                         | BUILTIN_FUNCTION
                         | TYPE_UNDEFINED
        """
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

    def p_arithmetic_expression(self, p: YaccProduction) -> None:
        """
        arithmetic_expression : expression PLUS expression
                              | expression MINUS expression
                              | expression MULTIPLICATION expression
                              | expression DIVISION expression
                              | expression MODULE expression
        """
        lhs, op, rhs = p[1:4]

        if (isinstance(lhs, ast.Integer) and not isinstance(rhs, ast.Integer)):
            raise ParserError(
                f"Invalid types for binary operator '{op}', " +
                "expected Integer and Integer, but got " +
                f"{type(lhs).__name__} and {type(rhs).__name__}",
                p.lineno(1)
            )

        if (isinstance(lhs, ast.String) and not isinstance(rhs, ast.String)):
            raise ParserError(
                f"Invalid types for binary operator '{op}', " +
                "expected String and String, but got " +
                f"{type(lhs).__name__} and {type(rhs).__name__}",
                p.lineno(1)
            )

        if op == '+':
            p[0] = ast.BinOp(lhs=lhs, op='+', rhs=rhs)
        elif op == '-':
            p[0] = ast.BinOp(lhs=lhs, op='-', rhs=rhs)
        elif op == '*':
            p[0] = ast.BinOp(lhs=lhs, op='*', rhs=rhs)
        elif op == '/':
            p[0] = ast.BinOp(lhs=lhs, op='/', rhs=rhs)

    # TODO: Find another way to parse these, lots of S/R conflicts.
    def p_comparison_expression(self, p: YaccProduction) -> None:
        """
        comparison_expression : expression LT expression
                              | expression IS_EQUAL_TO expression
                              | expression IS_NOT_EQUAL expression
                              | expression GREATER_THAN expression
        """
        p[0] = ast.BinOp(lhs=p[1], op=p[2], rhs=p[3])

    def p_if_expression(self, p: YaccProduction) -> None:
        """
        if_expression : IF LPAREN expression RPAREN expression ELSE expression
        """
        p[0] = ast.IfExpr(condition=p[3], ifBranch=p[5], elseBranch=p[7])

    def p_function_call(self, p: YaccProduction) -> None:
        """
        function_call : postfix_expression LPAREN function_args RPAREN
        """
        p[0] = ast.FunctionCall(name=p[1], args=p[3])

    def p_function_args(self, p: YaccProduction) -> None:
        """
        function_args : function_args expression COMMA
                      | function_args expression
                      | empty
        """
        if 3 <= len(p) <= 4:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = []

    def p_switch_expression(self, p: YaccProduction) -> None:
        """
        switch_expression : SWITCH LPAREN expression RPAREN LCURLY switch_branches RCURLY
        """
        p[0] = ast.SwitchExpr(target=p[3], branches=p[6])

    def p_switch_branches(self, p: YaccProduction) -> None:
        """
        switch_branches : switch_branch COMMA switch_branches
                        | switch_branch COMMA
                        | switch_branch
        """
        if 2 <= len(p) <= 3:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_switch_branch(self, p: YaccProduction) -> None:
        """
        switch_branch : switch_match_target FAT_ARROW expression
        """
        p[0] = ast.SwitchBranch(match=p[1], body=p[3])

    def p_switch_match_target(self, p: YaccProduction) -> None:
        """
        switch_match_target : switch_range
                            | switch_list
                            | ELSE
        """
        if p[1] == 'else':
            p[0] = ast.SwitchElse()
        else:
            p[0] = p[1]

    def p_switch_range(self, p: YaccProduction) -> None:
        """
        switch_range : INTEGER ELLIPSIS INTEGER
        """
        p[0] = ast.SwitchRange(start=p[1], end=p[3])

    def p_switch_list(self, p: YaccProduction) -> None:
        """
        switch_list : INTEGER COMMA switch_list
                    | INTEGER
        """
        if len(p) == 2:
            p[0] = ast.SwitchList(elems=[ast.Integer(p[1])])
        else:
            p[0] = ast.SwitchList(elems=[ast.Integer(p[1])] + p[3].elems)

    def p_struct_decl(self, p: YaccProduction) -> None:
        """
        struct_decl : STRUCT LCURLY struct_fields struct_methods RCURLY
        """
        p[0] = ast.StructDeclaration(fields=p[3], methods=p[4])

    def p_struct_fields(self, p: YaccProduction) -> None:
        """
        struct_fields : struct_fields struct_field COMMA
                      | empty
        """
        if len(p) == 4:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = []

    def p_struct_field(self, p: YaccProduction) -> None:
        """
        struct_field : IDENT COLON compound_typedecl
        """
        p[0] = ast.Identifier(p[1])

    def p_field_access(self, p: YaccProduction) -> None:
        """
        field_access : postfix_expression DOT IDENT
        """
        p[0] = ast.FieldAccess(
            target=p[1],
            field_name=ast.Identifier(p[3])
        )

    def p_struct_methods(self, p: YaccProduction) -> None:
        """
        struct_methods : struct_methods functiondecl_stmt
                       | empty
        """
        if len(p) == 3:
            p[0] = [p[2]] + p[1]
        else:
            p[0] = []

    def p_struct_instantiation(self, p: YaccProduction) -> None:
        """
        struct_instantiation : IDENT LCURLY struct_initializer_pairs RCURLY
                             | DOT LCURLY struct_initializer_pairs RCURLY
        """
        p[0] = ast.StructInstantiation(
            name=ast.Identifier(
                p[1]) if p[1] != '.' else ast.Identifier('anonymous'),
            field_initializers=p[3]
        )

    def p_struct_initializer_pairs(self, p: YaccProduction) -> None:
        """
        struct_initializer_pairs : struct_initializer_pair COMMA struct_initializer_pairs
                                 | struct_initializer_pair COMMA
                                 | struct_initializer_pair
        """
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]

    def p_struct_initializer_pair(self, p: YaccProduction) -> None:
        """
        struct_initializer_pair : struct_initializer_field_name EQUAL expression
        """
        p[0] = ast.StructInitializerPair(field_name=p[1], value=p[3])

    def p_struct_initializer_field_name(self, p: YaccProduction) -> None:
        """
        struct_initializer_field_name : DOT IDENT
        """
        p[0] = p[2]

    def p_for_stmt(self, p: YaccProduction) -> None:
        """
        for_stmt : FOR LPAREN expression RPAREN for_stmt_capture LCURLY stmts RCURLY
        """
        p[0] = ast.ForStmt(
            target=p[3],
            capture=p[5],
            body=p[7]
        )

    def p_for_stmt_capture(self, p: YaccProduction) -> None:
        """
        for_stmt_capture : BAR for_stmt_capture_target COMMA for_stmt_capture_target BAR
                         | BAR for_stmt_capture_target BAR
        """
        p[0] = ast.ForStmtCapture(
            item=p[2],
            index=p[4] if len(p) >= 5 else None
        )

    def p_for_stmt_capture_target(self, p: YaccProduction) -> None:
        """
        for_stmt_capture_target : IDENT
                                | UNDERSCORE
        """
        p[0] = ast.Identifier(p[1])

    def p_while_stmt(self, p: YaccProduction) -> None:
        """
        while_stmt : WHILE LPAREN expression RPAREN LCURLY stmts RCURLY
                   | WHILE LPAREN expression RPAREN BAR while_stmt_capture_target BAR LCURLY stmts RCURLY
                   | WHILE LPAREN expression RPAREN COLON LPAREN expression RPAREN LCURLY stmts RCURLY
        """
        condition = p[3]
        if len(p) == 8:
            p[0] = ast.WhileStmt(condition, body=p[6])
        elif len(p) == 9:
            p[0] = ast.WhileStmt(condition, capture=p[6], body=p[9])
        else:
            p[0] = ast.WhileStmt(condition, post_action=p[7], body=p[10])

    def p_while_stmt_capture_target(self, p: YaccProduction) -> None:
        """
        while_stmt_capture_target : IDENT
                                  | UNDERSCORE
        """
        p[0] = ast.Identifier(p[1])

    def p_try_expression(self, p: YaccProduction) -> None:
        """
        try_expression : TRY expression
        """
        p[0] = ast.TryExpr(p[2])

    def p_empty(self, _: YaccProduction) -> None:
        """empty :"""

    def p_error(self, token: LexToken) -> None:
        '''
        Skip tokens until we meet a synchronization point, a semicolon in this
        case.
        '''
        if not token:
            print('Unexpected end of file while parsing, maybe you forgot a semicolon?')
            return

        print(f'Error while parsing at token: {token.type}')

        while True:
            token = self.parser.token()
            if not token or token.type == 'SEMICOLON':
                break

        self.parser.restart()

    def p_enum_decl(self, p: YaccProduction) -> None:
        """
        enum_decl : ENUM LCURLY enum_variants enum_methods RCURLY
        """
        p[0] = ast.EnumDeclaration(
            variants=p[3],
            methods=p[4]
        )

    def p_enum_fields(self, p: YaccProduction) -> None:
        """
        enum_variants : enum_variants IDENT COMMA
                      | IDENT COMMA
        """
        if len(p) == 3:
            p[0] = [ast.Identifier(p[1])]
        else:
            p[0] = p[1] + [ast.Identifier(p[2])]

    def p_enum_methods(self, p: YaccProduction) -> None:
        """
        enum_methods : enum_methods functiondecl_stmt
                     | empty
        """
        p[0] = [] if len(p) == 2 else p[1] + [p[2]]

    def p_anon_array(self, p: YaccProduction) -> None:
        """
        anon_array : DOT LCURLY array_elems RCURLY
        """
        p[0] = ast.AnonArray(elems=p[3])

    def p_array_elems(self, p: YaccProduction) -> None:
        """
        array_elems : array_elems expression COMMA
                    | array_elems expression
                    | empty
        """
        if len(p) == 4:
            p[0] = p[1] + [p[2]]
        elif len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = []

    def parse(self, input: str) -> ast.Program:
        return cast(ast.Program, self.parser.parse(input, lexer=Lexer().lexer))
