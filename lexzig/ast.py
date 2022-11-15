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
class BinOp(Expr):
    lhs: Expr
    op: str
    rhs: Expr


class Stmt:
    pass


@dataclass
class AssignmentStmt(Stmt):
    ident: Identifier
    value: Expr


@dataclass
class Program:
    stmts: List[Stmt]
