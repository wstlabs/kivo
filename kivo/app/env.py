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

def show_root(env):
    modroot = env.moduleroot
    print("more?")
    print("known modules ..")
    head = ('name','version','active','kosher','sourced','firsterror')
    body = ((m.name,m.version,m.is_active,m.is_kosher,m.is_sourced,m.firsterror) for m in modroot.modules())
    rows = [head] + list(body)
    print(tabulate(rows,headers="firstrow"))
    print("decent modules ..")
    for m in modroot.modules():
        if m.is_kosher:
            print(f"name = {m.subpath}")
            if not m.is_sourced:
                continue
            for k in m.sources():
                config = m.source(k)
                print(f"source = {k} => {config}")

def show_index(env):
    index = env.moduleindex
    for name in index.sources():
        info = index.get(name)
        print(f"source = {name} => {info}")

def build_index(env):
    print("build ..")
    env.moduleindex.build()
    print("built.")

def main():
    args = parse_args()
    env = EnvironmentManager()
    print(env)
    print(tabulate(env.members()))
    if args.more:
        show_root(env)
    # build_index(env)
    if args.more:
        show_index(env)
    print("all done.")

if __name__ == '__main__':
    main()


