grammar Datalog;

datalogMain : mRule* ;

term
  : Constant   # Const
  | Identifier # Variable
  ;

atom : Identifier '(' term ')' ;

mRule : atom (':-' literals)? '.' ;

literal
  : atom     # LiteralAtom
  | '!' atom # LiteralNegAtom
  ;

literals : literal (',' literals)* ;

Identifier : ID_START ID_REST* ;

fragment ID_START : [a-zA-Z_] ;
fragment ID_REST : [a-zA-Z0-9_?] ;

Constant
  : '"' DoubleQuotedStringCharacter* '"'
  | '\'' SingleQuotedStringCharacter* '\'' ;

fragment
DoubleQuotedStringCharacter
  : ~["\r\n\\] | ('\\' .) ;

fragment
SingleQuotedStringCharacter
  : ~['\r\n\\] | ('\\' .) ;

WS : [ \t\r\n]+ -> skip ;
