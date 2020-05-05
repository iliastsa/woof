grammar Datalog;

datalogMain : mRule* ;

term
  : value=Constant   # Const
  | name=Identifier # Variable
  ;

atom : name=Identifier '(' terms=termList? ')' ;

termList
  : term (',' term)* ;

mRule : head=atom (':-' body=literals)? '.' ;

literal
  : atom     # LiteralAtom
  | '!' atom # LiteralNegAtom
  ;

literals : literal (',' literal)* ;

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
