import os
import argparse
from collections import OrderedDict
from tabulate import tabulate
from kivo.environment.manager import EnvironmentManager
from kivo.util.argparse import splitargv


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, required=True, help="source name")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--month", type=str, required=False, help="monthly version tag")
    g.add_argument("--year", type=str, required=False, help="yearly version tag")
    parser.add_argument("--dry", action="store_true")
    args = parser.parse_args()
    if args.month is not None:
        args.tempo = 'monthly'
        args.version = args.month
    if args.year is not None:
        args.tempo = 'yearly'
        args.version = args.year
    return args

def main():
    # args = parse_args()
    env = EnvironmentManager()
    print(env)
    print(tabulate(env.members()))

if __name__ == '__main__':
    main()


