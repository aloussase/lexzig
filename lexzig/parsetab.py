
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftMULTIPLICATIONDIVISIONAMPERSAND BANG BAR BUILTIN_FUNCTION CHAR COLON COMMA COMPTIME CONST DIVISION DIV_EQUAL DOT ELLIPSIS ELSE ENUM EQUAL EXPORT EXTERN FAT_ARROW FOR FUNCTION GREATER_THAN IDENT IF INTEGER IS_EQUAL_TO IS_NOT IS_NOT_EQUAL LBRACE LCURLY LPAREN LT MINUS MINUS_EQUAL MODULE MOD_EQUAL MULTIPLICATION MULT_EQUAL PLUS PLUS_EQUAL PUB RBRACE RCURLY RETURN RPAREN SEMICOLON STRING STRUCT SWITCH TEST THREADLOCAL TRY TYPE_ANYERROR TYPE_ANYOPAQUE TYPE_ANYTYPE TYPE_BOOL TYPE_COMPTIME_FLOAT TYPE_COMPTIME_INT TYPE_C_INT TYPE_C_LONG TYPE_C_LONGDOUBLE TYPE_C_LONGLONG TYPE_C_SHORT TYPE_C_UINT TYPE_C_ULONG TYPE_C_ULONGLONG TYPE_C_USHORT TYPE_F128 TYPE_F16 TYPE_F32 TYPE_F64 TYPE_F80 TYPE_I128 TYPE_I16 TYPE_I32 TYPE_I64 TYPE_I8 TYPE_ISIZE TYPE_NORETURN TYPE_NULL TYPE_TYPE TYPE_U128 TYPE_U16 TYPE_U32 TYPE_U64 TYPE_U8 TYPE_UNDEFINED TYPE_USIZE TYPE_VOID UNDERSCORE VAR WHILE\n        program : stmt stmts\n\n        stmts : stmt stmts\n              | empty\n        \n        stmt : assignment_stmt\n             | functiondecl_stmt\n        \n        assignment_stmt : vardecl IDENT assignment_stmt_tail\n                        | vardecl IDENT COLON typedecl assignment_stmt_tail\n\n        assignment_stmt_tail : EQUAL expression SEMICOLON\n        \n        functiondecl_stmt : function_signature function_body\n\n        param : IDENT colon_type\n\n        params_list : param\n                    | param COMMA params_list\n                    | empty\n\n        function_signature : access_modifier FUNCTION IDENT LPAREN params_list RPAREN typedecl\n\n        function_body : LCURLY stmts RCURLY\n        \n        colon_type : COLON typedecl\n                   | empty\n        \n        access_modifier : PUB\n                        | empty\n        \n        vardecl : VAR\n                | CONST\n                | COMPTIME\n        \n        typedecl : TYPE_I32\n                 | TYPE_I8\n                 | TYPE_U8\n                 | TYPE_I16\n                 | TYPE_U16\n                 | TYPE_U32\n                 | TYPE_I64\n                 | TYPE_U64\n                 | TYPE_I128\n                 | TYPE_U128\n                 | TYPE_ISIZE\n                 | TYPE_USIZE\n                 | TYPE_C_SHORT\n                 | TYPE_C_USHORT\n                 | TYPE_C_INT\n                 | TYPE_C_UINT\n                 | TYPE_C_LONG\n                 | TYPE_C_ULONG\n                 | TYPE_C_LONGLONG\n                 | TYPE_C_ULONGLONG\n                 | TYPE_C_LONGDOUBLE\n                 | TYPE_F16\n                 | TYPE_F32\n                 | TYPE_F64\n                 | TYPE_F80\n                 | TYPE_F128\n                 | TYPE_BOOL\n                 | TYPE_ANYOPAQUE\n                 | TYPE_VOID\n                 | TYPE_NORETURN\n                 | TYPE_TYPE\n                 | TYPE_ANYERROR\n                 | TYPE_ANYTYPE\n                 | TYPE_COMPTIME_INT\n                 | TYPE_COMPTIME_FLOAT\n                 | TYPE_NULL\n                 | TYPE_UNDEFINED\n        \n        expression : INTEGER PLUS INTEGER\n                   | INTEGER MINUS INTEGER\n                   | INTEGER MULTIPLICATION INTEGER\n                   | INTEGER DIVISION INTEGER\n                   | INTEGER\n        empty :'
    
_lr_action_items = {'VAR':([0,2,3,4,13,17,18,21,66,68,69,],[7,7,-4,-5,7,-9,7,-6,-15,-7,-8,]),'CONST':([0,2,3,4,13,17,18,21,66,68,69,],[8,8,-4,-5,8,-9,8,-6,-15,-7,-8,]),'COMPTIME':([0,2,3,4,13,17,18,21,66,68,69,],[9,9,-4,-5,9,-9,9,-6,-15,-7,-8,]),'PUB':([0,2,3,4,13,17,18,21,66,68,69,],[11,11,-4,-5,11,-9,11,-6,-15,-7,-8,]),'FUNCTION':([0,2,3,4,10,11,12,13,15,17,18,21,66,68,69,],[-65,-65,-4,-5,19,-18,-19,-65,-19,-9,-65,-6,-15,-7,-8,]),'$end':([1,2,3,4,13,14,15,17,20,21,66,68,69,],[0,-65,-4,-5,-65,-1,-3,-9,-2,-6,-15,-7,-8,]),'RCURLY':([3,4,13,15,17,18,20,21,24,66,68,69,],[-4,-5,-65,-3,-9,-65,-2,-6,66,-15,-7,-8,]),'IDENT':([5,7,8,9,19,67,86,],[16,-20,-21,-22,25,74,74,]),'LCURLY':([6,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,88,],[18,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-14,]),'COLON':([16,74,],[22,83,]),'EQUAL':([16,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,],[23,23,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,]),'TYPE_I32':([22,83,85,],[27,27,27,]),'TYPE_I8':([22,83,85,],[28,28,28,]),'TYPE_U8':([22,83,85,],[29,29,29,]),'TYPE_I16':([22,83,85,],[30,30,30,]),'TYPE_U16':([22,83,85,],[31,31,31,]),'TYPE_U32':([22,83,85,],[32,32,32,]),'TYPE_I64':([22,83,85,],[33,33,33,]),'TYPE_U64':([22,83,85,],[34,34,34,]),'TYPE_I128':([22,83,85,],[35,35,35,]),'TYPE_U128':([22,83,85,],[36,36,36,]),'TYPE_ISIZE':([22,83,85,],[37,37,37,]),'TYPE_USIZE':([22,83,85,],[38,38,38,]),'TYPE_C_SHORT':([22,83,85,],[39,39,39,]),'TYPE_C_USHORT':([22,83,85,],[40,40,40,]),'TYPE_C_INT':([22,83,85,],[41,41,41,]),'TYPE_C_UINT':([22,83,85,],[42,42,42,]),'TYPE_C_LONG':([22,83,85,],[43,43,43,]),'TYPE_C_ULONG':([22,83,85,],[44,44,44,]),'TYPE_C_LONGLONG':([22,83,85,],[45,45,45,]),'TYPE_C_ULONGLONG':([22,83,85,],[46,46,46,]),'TYPE_C_LONGDOUBLE':([22,83,85,],[47,47,47,]),'TYPE_F16':([22,83,85,],[48,48,48,]),'TYPE_F32':([22,83,85,],[49,49,49,]),'TYPE_F64':([22,83,85,],[50,50,50,]),'TYPE_F80':([22,83,85,],[51,51,51,]),'TYPE_F128':([22,83,85,],[52,52,52,]),'TYPE_BOOL':([22,83,85,],[53,53,53,]),'TYPE_ANYOPAQUE':([22,83,85,],[54,54,54,]),'TYPE_VOID':([22,83,85,],[55,55,55,]),'TYPE_NORETURN':([22,83,85,],[56,56,56,]),'TYPE_TYPE':([22,83,85,],[57,57,57,]),'TYPE_ANYERROR':([22,83,85,],[58,58,58,]),'TYPE_ANYTYPE':([22,83,85,],[59,59,59,]),'TYPE_COMPTIME_INT':([22,83,85,],[60,60,60,]),'TYPE_COMPTIME_FLOAT':([22,83,85,],[61,61,61,]),'TYPE_NULL':([22,83,85,],[62,62,62,]),'TYPE_UNDEFINED':([22,83,85,],[63,63,63,]),'INTEGER':([23,70,71,72,73,],[65,78,79,80,81,]),'LPAREN':([25,],[67,]),'COMMA':([27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,74,76,82,84,87,],[-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-65,86,-10,-17,-16,]),'RPAREN':([27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,67,74,75,76,77,82,84,86,87,89,],[-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-65,-65,85,-11,-13,-10,-17,-65,-16,-12,]),'SEMICOLON':([64,65,78,79,80,81,],[69,-64,-60,-61,-62,-63,]),'PLUS':([65,],[70,]),'MINUS':([65,],[71,]),'MULTIPLICATION':([65,],[72,]),'DIVISION':([65,],[73,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'stmt':([0,2,13,18,],[2,13,13,13,]),'assignment_stmt':([0,2,13,18,],[3,3,3,3,]),'functiondecl_stmt':([0,2,13,18,],[4,4,4,4,]),'vardecl':([0,2,13,18,],[5,5,5,5,]),'function_signature':([0,2,13,18,],[6,6,6,6,]),'access_modifier':([0,2,13,18,],[10,10,10,10,]),'empty':([0,2,13,18,67,74,86,],[12,15,15,15,77,84,77,]),'stmts':([2,13,18,],[14,20,24,]),'function_body':([6,],[17,]),'assignment_stmt_tail':([16,26,],[21,68,]),'typedecl':([22,83,85,],[26,87,88,]),'expression':([23,],[64,]),'params_list':([67,86,],[75,89,]),'param':([67,86,],[76,76,]),'colon_type':([74,],[82,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> stmt stmts','program',2,'p_program','parser.py',23),
  ('stmts -> stmt stmts','stmts',2,'p_program','parser.py',25),
  ('stmts -> empty','stmts',1,'p_program','parser.py',26),
  ('stmt -> assignment_stmt','stmt',1,'p_stmt','parser.py',31),
  ('stmt -> functiondecl_stmt','stmt',1,'p_stmt','parser.py',32),
  ('assignment_stmt -> vardecl IDENT assignment_stmt_tail','assignment_stmt',3,'p_assignment_stmt','parser.py',37),
  ('assignment_stmt -> vardecl IDENT COLON typedecl assignment_stmt_tail','assignment_stmt',5,'p_assignment_stmt','parser.py',38),
  ('assignment_stmt_tail -> EQUAL expression SEMICOLON','assignment_stmt_tail',3,'p_assignment_stmt','parser.py',40),
  ('functiondecl_stmt -> function_signature function_body','functiondecl_stmt',2,'p_functiondecl_stmt','parser.py',45),
  ('param -> IDENT colon_type','param',2,'p_functiondecl_stmt','parser.py',47),
  ('params_list -> param','params_list',1,'p_functiondecl_stmt','parser.py',49),
  ('params_list -> param COMMA params_list','params_list',3,'p_functiondecl_stmt','parser.py',50),
  ('params_list -> empty','params_list',1,'p_functiondecl_stmt','parser.py',51),
  ('function_signature -> access_modifier FUNCTION IDENT LPAREN params_list RPAREN typedecl','function_signature',7,'p_functiondecl_stmt','parser.py',53),
  ('function_body -> LCURLY stmts RCURLY','function_body',3,'p_functiondecl_stmt','parser.py',55),
  ('colon_type -> COLON typedecl','colon_type',2,'p_colon_type','parser.py',60),
  ('colon_type -> empty','colon_type',1,'p_colon_type','parser.py',61),
  ('access_modifier -> PUB','access_modifier',1,'p_access_modifier','parser.py',66),
  ('access_modifier -> empty','access_modifier',1,'p_access_modifier','parser.py',67),
  ('vardecl -> VAR','vardecl',1,'p_vardecl','parser.py',72),
  ('vardecl -> CONST','vardecl',1,'p_vardecl','parser.py',73),
  ('vardecl -> COMPTIME','vardecl',1,'p_vardecl','parser.py',74),
  ('typedecl -> TYPE_I32','typedecl',1,'p_typedecl','parser.py',80),
  ('typedecl -> TYPE_I8','typedecl',1,'p_typedecl','parser.py',81),
  ('typedecl -> TYPE_U8','typedecl',1,'p_typedecl','parser.py',82),
  ('typedecl -> TYPE_I16','typedecl',1,'p_typedecl','parser.py',83),
  ('typedecl -> TYPE_U16','typedecl',1,'p_typedecl','parser.py',84),
  ('typedecl -> TYPE_U32','typedecl',1,'p_typedecl','parser.py',85),
  ('typedecl -> TYPE_I64','typedecl',1,'p_typedecl','parser.py',86),
  ('typedecl -> TYPE_U64','typedecl',1,'p_typedecl','parser.py',87),
  ('typedecl -> TYPE_I128','typedecl',1,'p_typedecl','parser.py',88),
  ('typedecl -> TYPE_U128','typedecl',1,'p_typedecl','parser.py',89),
  ('typedecl -> TYPE_ISIZE','typedecl',1,'p_typedecl','parser.py',90),
  ('typedecl -> TYPE_USIZE','typedecl',1,'p_typedecl','parser.py',91),
  ('typedecl -> TYPE_C_SHORT','typedecl',1,'p_typedecl','parser.py',92),
  ('typedecl -> TYPE_C_USHORT','typedecl',1,'p_typedecl','parser.py',93),
  ('typedecl -> TYPE_C_INT','typedecl',1,'p_typedecl','parser.py',94),
  ('typedecl -> TYPE_C_UINT','typedecl',1,'p_typedecl','parser.py',95),
  ('typedecl -> TYPE_C_LONG','typedecl',1,'p_typedecl','parser.py',96),
  ('typedecl -> TYPE_C_ULONG','typedecl',1,'p_typedecl','parser.py',97),
  ('typedecl -> TYPE_C_LONGLONG','typedecl',1,'p_typedecl','parser.py',98),
  ('typedecl -> TYPE_C_ULONGLONG','typedecl',1,'p_typedecl','parser.py',99),
  ('typedecl -> TYPE_C_LONGDOUBLE','typedecl',1,'p_typedecl','parser.py',100),
  ('typedecl -> TYPE_F16','typedecl',1,'p_typedecl','parser.py',101),
  ('typedecl -> TYPE_F32','typedecl',1,'p_typedecl','parser.py',102),
  ('typedecl -> TYPE_F64','typedecl',1,'p_typedecl','parser.py',103),
  ('typedecl -> TYPE_F80','typedecl',1,'p_typedecl','parser.py',104),
  ('typedecl -> TYPE_F128','typedecl',1,'p_typedecl','parser.py',105),
  ('typedecl -> TYPE_BOOL','typedecl',1,'p_typedecl','parser.py',106),
  ('typedecl -> TYPE_ANYOPAQUE','typedecl',1,'p_typedecl','parser.py',107),
  ('typedecl -> TYPE_VOID','typedecl',1,'p_typedecl','parser.py',108),
  ('typedecl -> TYPE_NORETURN','typedecl',1,'p_typedecl','parser.py',109),
  ('typedecl -> TYPE_TYPE','typedecl',1,'p_typedecl','parser.py',110),
  ('typedecl -> TYPE_ANYERROR','typedecl',1,'p_typedecl','parser.py',111),
  ('typedecl -> TYPE_ANYTYPE','typedecl',1,'p_typedecl','parser.py',112),
  ('typedecl -> TYPE_COMPTIME_INT','typedecl',1,'p_typedecl','parser.py',113),
  ('typedecl -> TYPE_COMPTIME_FLOAT','typedecl',1,'p_typedecl','parser.py',114),
  ('typedecl -> TYPE_NULL','typedecl',1,'p_typedecl','parser.py',115),
  ('typedecl -> TYPE_UNDEFINED','typedecl',1,'p_typedecl','parser.py',116),
  ('expression -> INTEGER PLUS INTEGER','expression',3,'p_expression','parser.py',121),
  ('expression -> INTEGER MINUS INTEGER','expression',3,'p_expression','parser.py',122),
  ('expression -> INTEGER MULTIPLICATION INTEGER','expression',3,'p_expression','parser.py',123),
  ('expression -> INTEGER DIVISION INTEGER','expression',3,'p_expression','parser.py',124),
  ('expression -> INTEGER','expression',1,'p_expression','parser.py',125),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',145),
]
