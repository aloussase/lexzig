import unittest

from lexzig.ast import (Program, FunctionDeclStmt, Identifier, AssignmentStmt,
                        Integer, IfExpr, BinOp, SwitchExpr, SwitchBranch,
                        SwitchRange, SwitchList, FunctionCall,
                        SwitchElse, ReturnStmt, StructDeclaration,
                        StructInstantiation, StructInitializerPair,
                        String, FieldAccess, ForStmt, ForStmtCapture, TryExpr,
                        UnaryOp, WhileStmt, AssignmentExpr, EnumDeclaration,
                        Char, AnonArray
                        )
from lexzig.parser import Parser


class TestParser(unittest.TestCase):
    parser = Parser()

    # TODO: Test arithmetic expressions
    # TODO: Test comparison operators

    def test_parser_can_parse_anon_arrays(self):
        input = "const x: [_]u8 = .{'h', 'e', 'l', 'l', 'o'};"
        expected = Program(stmts=[AssignmentStmt(
            Identifier('x'),
            AnonArray(elems=[
                Char("'h'"),
                Char("'e'"),
                Char("'l'"),
                Char("'l'"),
                Char("'o'")
            ])
        )])

        result = self.parser.parse(input)

        self.assertEqual(expected, result)

    def test_parser_can_parse_enums(self):
        input = '''
        const RGB = enum {
            Red,
            Green,
            Blue,
        };
        '''
        expected = Program(stmts=[AssignmentStmt(Identifier('RGB'), EnumDeclaration(
            variants=[
                Identifier('Red'),
                Identifier('Green'),
                Identifier('Blue')
            ],
            methods=[],
        ))])

        result = self.parser.parse(input)

        self.assertEqual(expected, result)

    def test_parser_can_parse_while_loops(self):
        input = '''
        var x = 1;
        while (x < 10) : (x += 1) {
            std.debug.print("x = {}", .{x});
        }
        '''
        expected = Program(stmts=[
            AssignmentStmt(Identifier('x'), Integer(1)),
            WhileStmt(
                condition=BinOp(Identifier('x'), '<', Integer(10)),
                post_action=AssignmentExpr(
                    ident=Identifier('x'),
                    op='+=',
                    value=Integer(1)
                ),
                body=[FunctionCall(
                    FieldAccess(
                        FieldAccess(Identifier("std"), Identifier("debug")),
                        Identifier("print")
                    ),
                    args=[
                        String("\"x = {}\""),
                        AnonArray(elems=[Identifier('x')])
                    ]
                )])
        ])

        result = self.parser.parse(input)

        self.assertEqual(expected, result)

    def test_parser_can_parse_ampersand(self):
        input = '&someVariable;'
        expected = Program(stmts=[
            UnaryOp(op='&', rhs=Identifier('someVariable'))
        ])

        result = self.parser.parse(input)

        self.assertEqual(expected, result)

    def test_parser_can_parse_try_expressions(self):
        input = '''const x = try someFunc();'''
        expected = Program(stmts=[
            AssignmentStmt(
                Identifier('x'),
                TryExpr(FunctionCall(Identifier('someFunc'), []))
            )
        ])

        result = self.parser.parse(input)

        self.assertEqual(expected, result)

    def test_parser_can_parse_for_loops_with_only_item_capture(self):
        input = '''
        for (string) |character| {
            _ = character;
        }
        '''
        expected = Program(stmts=[
            ForStmt(
                target=Identifier('string'),
                capture=ForStmtCapture(
                    item=Identifier('character'),
                    index=None
                ),
                body=[
                    AssignmentStmt(Identifier('_'), Identifier('character'))
                ]
            )
        ])

        result = self.parser.parse(input)

        self.assertEqual(expected, result)

    def test_parser_can_parse_for_loops_with_both_item_and_index_captures(self):
        input = '''
        for (string) |character, index| {
            _ = character;
            _ = index;
        }
        '''
        expected = Program(stmts=[ForStmt(
            target=Identifier('string'),
            capture=ForStmtCapture(
                item=Identifier('character'),
                index=Identifier('index'),
            ),
            body=[
                AssignmentStmt(Identifier('_'), Identifier('character')),
                AssignmentStmt(Identifier('_'), Identifier('index'))
            ]
        )
        ])

        result = self.parser.parse(input)

        self.assertEqual(expected, result)

    def test_parser_can_parse_functions_with_export_modifiers(self):
        input = '''
        pub export fn div(x: i32, y: i32) i32 {
            return x / y; 
        }
        '''

        result = self.parser.parse(input)

        self.assertEqual(Program(stmts=[FunctionDeclStmt(
            name=Identifier('div'),
            params=[Identifier('x'), Identifier('y')],
            body=[ReturnStmt(value=BinOp(
                Identifier('x'), '/', Identifier('y')))]
        )]), result)

    def test_parser_can_parse_variables_with_export_modifiers(self):
        input = 'export var x = 42;'

        result = self.parser.parse(input)

        self.assertEqual(Program(stmts=[
            AssignmentStmt(ident=Identifier('x'), value=Integer(42))
        ]), result)

    def test_parser_can_parse_method_call(self):
        input = 'std.debug.print("Hello");'
        expected = Program(stmts=[
            FunctionCall(
                name=FieldAccess(
                    target=FieldAccess(target=Identifier(
                        'std'), field_name=Identifier('debug')),
                    field_name=Identifier("print")
                ),
                args=[String("\"Hello\"")]
            )])

        result = self.parser.parse(input)

        self.assertEqual(expected, result)

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
                    SwitchBranch(match=SwitchRange(
                        start=0, end=1), body=Integer(20)),
                    SwitchBranch(match=SwitchList(elems=[Integer(10), Integer(100)]),
                                 body=FunctionCall(name=Identifier('divExact'), args=[Integer(10), Integer(10)])),
                    SwitchBranch(match=SwitchElse(), body=Integer(10))
                ]
            ))
        ]), result)

    def test_parser_can_parse_return_stmts(self):
        input = 'return 42;'

        result = self.parser.parse(input)

        self.assertEqual(
            Program(stmts=[ReturnStmt(value=Integer(42))]), result)

    def test_parser_can_parse_anonymous_struct_instantiation(self):
        input = '''
        const x: Person = .{
            .name = "John",
            .lastName = "Doe",
        };
        '''
        expected = Program(stmts=[AssignmentStmt(
            Identifier('x'),
            StructInstantiation(
                name=Identifier("anonymous"),
                field_initializers=[
                    StructInitializerPair('name', String('\"John\"')),
                    StructInitializerPair('lastName', String('\"Doe\"'))
                ]))
        ])

        result = self.parser.parse(input)

        self.assertEqual(expected, result)

    def test_parser_can_parse_structs(self):
        input = '''
        const Circle = struct {
            x: i32,
            y: i32,

            pub fn new(x: i32, y: i32) Circle {
                return Circle{
                    .x = x,
                    .y = y
                };
            }
        };
        '''

        result = self.parser.parse(input)

        self.assertEqual(Program(stmts=[
            AssignmentStmt(ident=Identifier('Circle'), value=StructDeclaration(
                fields=[Identifier('x'), Identifier('y')],
                methods=[
                    FunctionDeclStmt(
                        name=Identifier('new'),
                        params=[Identifier('x'), Identifier('y')],
                        body=[
                            ReturnStmt(value=StructInstantiation(
                                name=Identifier('Circle'),
                                field_initializers=[
                                    StructInitializerPair(
                                        'x', Identifier('x')),
                                    StructInitializerPair('y', Identifier('y'))
                                ],
                            ))
                        ]
                    )
                ]
            ))
        ]), result)
