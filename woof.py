#!/usr/bin/env python3
import argparse
import os

from antlr4 import FileStream

from src.engine.engine import Engine

parser = argparse.ArgumentParser(description='Woof: An interpreter for Datalog with Well Founded semantics.')

parser.add_argument(
    'file',
    metavar='F',
    type=str,
    help='Woof Datalog program file'
)

parser.add_argument(
    '--print',
    action='store_true',
    required=False,
    default=False,
    dest='print',
    help='Print true and unknown facts to stdout'
)

parser.add_argument(
    '--output',
    type=str,
    required=False,
    default=None,
    dest='output_dir',
    help='If specified, true and unknown facts will be output in the directory',
)

args = parser.parse_args()

if __name__ == '__main__':
    engine = Engine(FileStream(args.file))

    engine.run()

    if args.print:
        engine.print_all()

    if args.output_dir:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)

        engine.output_all(args.output_dir)
