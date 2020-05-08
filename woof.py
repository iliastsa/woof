#!/usr/bin/env python3
import argparse

from antlr4 import FileStream

from src.engine.engine import Engine

parser = argparse.ArgumentParser(description='Woof: An interpreter for Datalog with Well Founded semantics.')
parser.add_argument(
    'file',
    metavar='F',
    type=str,
    help='Woof Datalog program file'
)

args = parser.parse_args()

if __name__ == '__main__':
    engine = Engine(FileStream(args.file))

    true_facts, t_u_dk = engine.run()

    for i, p in true_facts.items():
        print(f'{i}: ', p)
