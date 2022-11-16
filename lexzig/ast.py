from dataclasses import dataclass
from typing import List


class Expr:
    pass


@dataclass
class Identifier:
    name: str


@dataclass
class Integer(Expr):
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


class Stmt:
    pass


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
class Program:
    stmts: List[Stmt]
