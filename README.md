# Woof
A Datalog interpreter implementing the Well-Founded semantics.

# Prerequisites
To install the required Python packages, run:
```shell
pip install -r requirements.txt
```

This project also requires you to have antlr4 installed and have the antlr jar path in the classpath.

Once that has been done, you can generate the parser by running:
```shell
make
```

# Usage
The simplest command for invoking Woof is:
```shell
./woof.py WOOF_FILE
```

This will run the interpreter on the input file, but produce no output. To view the possible flags and output options,
run:
```shell
./woof.py -h
```

The syntax of a valid Woof Datalog program is defined [here](src/parser/Datalog.g4)
