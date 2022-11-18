import unittest

from lexzig.ast import (Program, FunctionDeclStmt, Identifier, AssignmentStmt,
                        Integer, IfExpr, BinOp, SwitchExpr, SwitchBranch, SwitchRange, SwitchList, FunctionCall,
                        SwitchElse, ReturnStmt
                        )
from lexzig.parser import Parser


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

    def test_parser_can_parse_switch_expressions(self):
        input = '''
        var x = switch (10) {
            0...1 => 20,
            10, 100 => @divExact(10, 10),
            else => 10,
        };
        '''

        result = self.parser.parse(input)

        self.assertEqual(Program(stmts=[
            AssignmentStmt(ident=Identifier('x'), value=SwitchExpr(
                target=Integer(10),
                branches=[
                    SwitchBranch(match=SwitchRange(start=0, end=1), body=Integer(20)),
                    SwitchBranch(match=SwitchList(elems=[Integer(10), Integer(100)]),
                                 body=FunctionCall(name=Identifier('divExact'), args=[Integer(10), Integer(10)])),
                    SwitchBranch(match=SwitchElse(), body=Integer(10))
                ]
            ))
        ]), result)

    def test_parser_can_parse_return_stmts(self):
        input = 'return 42;'

        result = self.parser.parse(input)

        self.assertEqual(Program(stmts=[ReturnStmt(value=Integer(42))]), result)
