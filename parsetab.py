
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'CLASS CLOSE_BRACE CLOSE_PAREN COMMA DOT EQUAL FOR FOR ID INT LBRACKET LT MAIN NUMBER OPEN_BRACE OPEN_PAREN PLUS PLUSPLUS PRINTLN PRINTLN PUBLIC RBRACKET SEMICOLON STATIC STRING STRING_LITERAL VOIDprogram : PUBLIC CLASS ID OPEN_BRACE main_method CLOSE_BRACEmain_method : PUBLIC STATIC VOID MAIN OPEN_PAREN STRING LBRACKET RBRACKET ID CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACEstatement_list : statement\n                      | statement_list statementstatement : println_statement\n                 | for_statementprintln_statement : PRINTLN OPEN_PAREN STRING_LITERAL CLOSE_PAREN SEMICOLONfor_statement : FOR OPEN_PAREN INT ID EQUAL NUMBER SEMICOLON ID LT NUMBER SEMICOLON ID PLUSPLUS CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE'
    
_lr_action_items = {'PUBLIC':([0,5,],[2,6,]),'$end':([1,9,],[0,-1,]),'CLASS':([2,],[3,]),'ID':([3,15,30,36,40,],[4,16,32,37,41,]),'OPEN_BRACE':([4,17,43,],[5,18,44,]),'STATIC':([6,],[8,]),'CLOSE_BRACE':([7,19,20,21,22,25,26,33,45,46,],[9,25,-3,-5,-6,-2,-4,-7,46,-8,]),'VOID':([8,],[10,]),'MAIN':([10,],[11,]),'OPEN_PAREN':([11,23,24,],[12,27,28,]),'STRING':([12,],[13,]),'LBRACKET':([13,],[14,]),'RBRACKET':([14,],[15,]),'CLOSE_PAREN':([16,29,42,],[17,31,43,]),'PRINTLN':([18,19,20,21,22,26,33,44,45,46,],[23,23,-3,-5,-6,-4,-7,23,23,-8,]),'FOR':([18,19,20,21,22,26,33,44,45,46,],[24,24,-3,-5,-6,-4,-7,24,24,-8,]),'STRING_LITERAL':([27,],[29,]),'INT':([28,],[30,]),'SEMICOLON':([31,35,39,],[33,36,40,]),'EQUAL':([32,],[34,]),'NUMBER':([34,38,],[35,39,]),'LT':([37,],[38,]),'PLUSPLUS':([41,],[42,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'main_method':([5,],[7,]),'statement_list':([18,44,],[19,45,]),'statement':([18,19,44,45,],[20,26,20,26,]),'println_statement':([18,19,44,45,],[21,21,21,21,]),'for_statement':([18,19,44,45,],[22,22,22,22,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PUBLIC CLASS ID OPEN_BRACE main_method CLOSE_BRACE','program',6,'p_program','app.py',65),
  ('main_method -> PUBLIC STATIC VOID MAIN OPEN_PAREN STRING LBRACKET RBRACKET ID CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE','main_method',13,'p_main_method','app.py',69),
  ('statement_list -> statement','statement_list',1,'p_statement_list','app.py',73),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','app.py',74),
  ('statement -> println_statement','statement',1,'p_statement','app.py',81),
  ('statement -> for_statement','statement',1,'p_statement','app.py',82),
  ('println_statement -> PRINTLN OPEN_PAREN STRING_LITERAL CLOSE_PAREN SEMICOLON','println_statement',5,'p_println_statement','app.py',86),
  ('for_statement -> FOR OPEN_PAREN INT ID EQUAL NUMBER SEMICOLON ID LT NUMBER SEMICOLON ID PLUSPLUS CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE','for_statement',17,'p_for_statement','app.py',90),
]