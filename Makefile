ANTLR4 := /usr/local/lib/antlr-4.8-complete.jar

parser: src/parser/Datalog.g4
	@java -Xmx500M -cp ${ANTLR4}:${CLASSPATH} org.antlr.v4.Tool -Dlanguage=Python3 -no-listener -visitor -Xexact-output-dir -o src/parser/antlr/ src/parser/Datalog.g4