from dataclasses import dataclass
from typing import List, Optional, Any, Callable


def ast_node(name: str) -> Callable[[Any], Any]:
    """
    Attach the type of node to an ast node.
    """

    def inner(self: Any) -> Any:
        if hasattr(self, '__annotations__'):
            self.__annotations__['type'] = str
        setattr(self, 'type', name)
        return self

    return inner


@dataclass
@ast_node("stmt")
class Stmt:
    pass


@dataclass
@ast_node("expr")
class Expr(Stmt):
    pass


@ast_node("switch_match_target")
class SwitchMatchTarget:
    pass


@dataclass
@ast_node("identifier")
class Identifier(Expr):
    name: str


@dataclass
@ast_node("integer")
class Integer(Expr, SwitchMatchTarget):
    n: int


@dataclass
@ast_node("string")
class String(Expr):
    s: str


@dataclass
@ast_node("char")
class Char(Expr):
    c: str


@dataclass
@ast_node("binary_op")
class BinOp(Expr):
    lhs: Expr
    op: str
    rhs: Expr


@dataclass
@ast_node("unary_op")
class UnaryOp(Expr):
    op: str
    rhs: Expr


@dataclass
@ast_node("if_expression")
class IfExpr(Expr):
    condition: Expr
    ifBranch: Expr
    elseBranch: Expr


@dataclass
@ast_node("switch_range")
class SwitchRange(SwitchMatchTarget):
    start: int
    end: int


@dataclass
@ast_node("switch_list")
class SwitchList(SwitchMatchTarget):
    elems: List[SwitchMatchTarget]


@dataclass
@ast_node("switch_else")
class SwitchElse(SwitchMatchTarget):
    pass


@dataclass
@ast_node("switch_branch")
class SwitchBranch:
    match: SwitchMatchTarget
    body: Expr


@dataclass
@ast_node("switch_expression")
class SwitchExpr(Expr):
    target: Expr
    branches: List[SwitchBranch]


@dataclass
@ast_node("function_call")
class FunctionCall(Expr):
    name: Expr
    args: List[Expr]


@dataclass
@ast_node("assignment_stmt")
class AssignmentStmt(Stmt):
    ident: Identifier
    value: Expr


@dataclass
@ast_node("function_declaration_stmt")
class FunctionDeclStmt(Stmt):
    name: Identifier
    params: List[Identifier]
    body: List[Stmt]


@dataclass
@ast_node("return_stmt")
class ReturnStmt(Stmt):
    value: Expr


@dataclass
@ast_node("enum")
class EnumDeclaration(Expr):
    variants: List[Identifier]
    methods: List[FunctionDeclStmt]


@dataclass
@ast_node("struct")
class StructDeclaration(Expr):
    fields: List[Identifier]
    methods: List[FunctionDeclStmt]


@dataclass
@ast_node("struct_initializer_pair")
class StructInitializerPair:
    field_name: str
    value: Expr


@dataclass
@ast_node("struct_instantiation")
class StructInstantiation(Expr):
    name: Identifier
    field_initializers: List[StructInitializerPair]


@dataclass
@ast_node("field_access")
class FieldAccess(Expr):
    target: Expr
    field_name: Identifier


@dataclass
@ast_node("for_stmt_capture")
class ForStmtCapture:
    item: Identifier
    index: Optional[Identifier]


@dataclass
@ast_node("for_stmt")
class ForStmt(Stmt):
    target: Identifier
    capture: ForStmtCapture
    body: List[Stmt]


@dataclass
@ast_node("try_expression")
class TryExpr(Expr):
    value: Expr


@dataclass
@ast_node("while_stmt")
class WhileStmt(Stmt):
    condition: Expr
    body: List[Stmt]
    post_action: Optional[Expr] = None
    capture: Optional[Identifier] = None


@dataclass
@ast_node("assignment_expression")
class AssignmentExpr(Expr):
    ident: Identifier
    op: str
    value: Expr


@dataclass
@ast_node("anon_array")
class AnonArray(Expr):
    elems: List[Expr]


@dataclass
@ast_node("program")
class Program:
    stmts: List[Stmt]
