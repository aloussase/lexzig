from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Stmt:
    type = "stmt"
    pass


@dataclass
class Expr(Stmt):
    type = "expr"
    pass


class SwitchMatchTarget:
    type = "switch-match-target"
    pass


@dataclass
class Identifier(Expr):
    type = "identifier"
    name: str


@dataclass
class Integer(Expr, SwitchMatchTarget):
    type = "integer"
    n: int


@dataclass
class String(Expr):
    type = "string"
    s: str


@dataclass
class Char(Expr):
    type = "char"
    c: str


@dataclass
class BinOp(Expr):
    type = "binary-op"
    lhs: Expr
    op: str
    rhs: Expr


@dataclass
class UnaryOp(Expr):
    type = "unary-op"
    op: str
    rhs: Expr


@dataclass
class IfExpr(Expr):
    type = "if-expression"
    condition: Expr
    ifBranch: Expr
    elseBranch: Expr


@dataclass
class SwitchRange(SwitchMatchTarget):
    type = "switch-range"
    start: int
    end: int


@dataclass
class SwitchList(SwitchMatchTarget):
    type = "switch-list"
    elems: List[SwitchMatchTarget]


@dataclass
class SwitchElse(SwitchMatchTarget):
    type = "switch-else"
    pass


@dataclass
class SwitchBranch:
    type = "switch-branch"
    match: SwitchMatchTarget
    body: Expr


@dataclass
class SwitchExpr(Expr):
    type = "switch-expr"
    target: Expr
    branches: List[SwitchBranch]


@dataclass
class FunctionCall(Expr):
    type = "function-call"
    name: Expr
    args: List[Expr]


@dataclass
class AssignmentStmt(Stmt):
    type = "assignment-stmt"
    ident: Identifier
    value: Expr


@dataclass
class FunctionDeclStmt(Stmt):
    type = "functiondecl-stmt"
    name: Identifier
    params: List[Identifier]
    body: List[Stmt]


@dataclass
class ReturnStmt(Stmt):
    type = "return-stmt"
    value: Expr


@dataclass
class EnumDeclaration(Expr):
    type = "enum-decl"
    variants: List[Identifier]
    methods: List[FunctionDeclStmt]


@dataclass
class StructDeclaration(Expr):
    type = "struct-decl"
    fields: List[Identifier]
    methods: List[FunctionDeclStmt]


@dataclass
class StructInitializerPair:
    type = "struct-initialization-pair"
    field_name: str
    value: Expr


@dataclass
class StructInstantiation(Expr):
    type = "struct-instantiation"
    name: Identifier
    field_initializers: List[StructInitializerPair]


@dataclass
class FieldAccess(Expr):
    type = "field-access"
    target: Expr
    field_name: Identifier


@dataclass
class ForStmtCapture:
    type = "for-stmt-capture"
    item: Identifier
    index: Optional[Identifier]


@dataclass
class ForStmt(Stmt):
    type = "for-stmt"
    target: Identifier
    capture: ForStmtCapture
    body: List[Stmt]


@dataclass
class TryExpr(Expr):
    type = "try-expr"
    value: Expr


@dataclass
class WhileStmt(Stmt):
    type = "while-stmt"
    condition: Expr
    body: List[Stmt]
    post_action: Optional[Expr] = None
    capture: Optional[Identifier] = None


@dataclass
class AssignmentExpr(Expr):
    type = "assignment-expr"
    ident: Identifier
    op: str
    value: Expr


@dataclass
class AnonArray(Expr):
    elems: List[Expr]


@dataclass
class Program:
    type = "program-stmt"
    stmts: List[Stmt]
