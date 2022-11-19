from dataclasses import dataclass
from typing import List


@dataclass
class Stmt:
    pass


@dataclass
class Expr(Stmt):
    pass


class SwitchMatchTarget: pass


@dataclass
class Identifier(Expr):
    name: str


@dataclass
class Integer(Expr, SwitchMatchTarget):
    n: int


@dataclass
class String(Expr):
    s: str


@dataclass
class Char(Expr):
    c: str


@dataclass
class BinOp(Expr):
    lhs: Expr
    op: str
    rhs: Expr


@dataclass
class IfExpr(Expr):
    condition: Expr
    ifBranch: Expr
    elseBranch: Expr


@dataclass
class SwitchRange(SwitchMatchTarget):
    start: int
    end: int


@dataclass
class SwitchList(SwitchMatchTarget):
    elems: List[SwitchMatchTarget]


@dataclass
class SwitchElse(SwitchMatchTarget): pass


@dataclass
class SwitchBranch:
    match: SwitchMatchTarget
    body: Expr


@dataclass
class SwitchExpr(Expr):
    target: Expr
    branches: List[SwitchBranch]


@dataclass
class FunctionCall(Expr):
    name: Expr
    args: List[Expr]


@dataclass
class AssignmentStmt(Stmt):
    ident: Identifier
    value: Expr


@dataclass
class FunctionDeclStmt(Stmt):
    name: Identifier
    params: List[Identifier]
    body: List[Stmt]


@dataclass
class ReturnStmt(Stmt):
    value: Expr


@dataclass
class StructDeclaration(Expr):
    fields: List[Identifier]
    methods: List[FunctionDeclStmt]


@dataclass
class StructInitializerPair:
    field_name: str
    value: Expr


@dataclass
class StructInstantiation(Expr):
    name: Identifier
    field_initializers: List[StructInitializerPair]


@dataclass
class FieldAccess(Expr):
    target: Expr
    field_name: Identifier


@dataclass
class Program:
    stmts: List[Stmt]
