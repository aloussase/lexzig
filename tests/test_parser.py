import unittest

from lexzig.parser import Parser
from lexzig.ast import (Program, FunctionDeclStmt, Identifier, AssignmentStmt,
                        Integer, IfExpr, BinOp
                        )


class TestParser(unittest.TestCase):
    parser = Parser()

    def test_parser_can_parse_function_declarations(self):
        input = '''
        pub fn main(args: []u8) void {
            const x = 42;
        }
        '''

        result = self.parser.parse(input)

        self.assertEqual(
            Program(stmts=[
                    FunctionDeclStmt(
                        name=Identifier(name='main'),
                        params=[Identifier('args')],
                        body=[
                            AssignmentStmt(
                                ident=Identifier('x'), value=Integer(42)
                            )
                        ],
                    ),
                    ]), result)

    def test_parser_can_parse_variable_declarations(self):
        input = '''
        var x = 1;
        const y = 2;
        comptime z = 3;
        '''

        result = self.parser.parse(input)

        self.assertEqual(
            Program(stmts=[
                    AssignmentStmt(ident=Identifier('x'), value=Integer(1)),
                    AssignmentStmt(ident=Identifier('y'), value=Integer(2)),
                    AssignmentStmt(ident=Identifier('z'), value=Integer(3)),
                    ]), result)

    def test_parser_can_parse_if_expressions(self):
        input = 'if (9 < 10) 42 else 69;'

        result = self.parser.parse(input)

        self.assertEqual(
            Program(stmts=[
                IfExpr(
                    condition=BinOp(Integer(9), '<', Integer(10)),
                    ifBranch=Integer(42),
                    elseBranch=Integer(69),
                )
            ]), result)

    def test_parser_can_parser_underscore_assignment(self):
        input = '_ = x;'

        result = self.parser.parse(input)

        self.assertEqual(
            Program(stmts=[
                AssignmentStmt(ident=Identifier('_'), value=Identifier('x'))
            ]), result)
