parser: src/parser/Datalog.g4
	@java -Xmx500M -cp ${CLASSPATH} org.antlr.v4.Tool -Dlanguage=Python3 -no-listener -visitor -Xexact-output-dir -o src/parser/antlr/ src/parser/Datalog.g4

clean:
	rm -rf src/parser/antlr/*
