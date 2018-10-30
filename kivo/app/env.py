import os
import argparse
from tabulate import tabulate
from kivo.environment.manager import EnvironmentManager

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--more", action="store_true", help="strip all columns")
    return parser.parse_args()

def softver(module):
    return module.version if module.is_kosher else None

def show_more(env):
    modroot = env.moduleroot
    print("more?")
    print("known modules ..")
    tags = ((str(m),m.is_active,m.is_kosher,softver(m)) for m in modroot.modules())
    print(tabulate(tags))

def main():
    args = parse_args()
    env = EnvironmentManager()
    print(env)
    print(tabulate(env.members()))
    if args.more:
        show_more(env)
    print("all done.")

if __name__ == '__main__':
    main()


import argparse
