import os
import argparse
from tabulate import tabulate
from ..logging import log
from kivo.environment.manager import EnvironmentManager

def source2table(source,schema='t0'):
    table = source.replace('-','_')
    return f"{schema}.{table}"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, required=True, help="source name")
    parser.add_argument("--version", type=str, required=False, help="version tag")
    parser.add_argument("--more", action="store_true", help="strip all columns")
    # parser.add_argument("--dry", action="store_true")
    return parser.parse_args()

def logfiles(source,version):
    pid = os.getpid()
    logbase=f"{source}--{version}--{pid}"
    if not os.path.exists(LOGDIR):
        os.mkdir(LOGDIR)
    outfile=f"{LOGDIR}/err--{logbase}.txt"
    errfile=f"{LOGDIR}/out--{logbase}.txt"
    return outfile,errfile

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
                source = m.source(k)
                print(f"source = {k} => {source}")

def show_index(env):
    index = env.moduleindex
    for name in index.sources():
        source = index.get(name)
        d = source.as_dict()
        print(f"source = {name} => {d}")

def build_index(env):
    print("build ..")
    env.moduleindex.build()
    print("built.")

def __mkargs_stage(pgconf,stage,source,label='current'):
    infile = stage.fullpath(f"{label}/{source}.csv")
    log.info(f"infile = {infile}")
    print(f"infile = {infile}")
    if not os.path.exists(infile):
        raise ValueError(f"can't find infile '{infile}'")
    print(f"source = {source}")
    table = source2table(source)
    print(f"table = {table}")
    print(f"pgconf = {pgconf}")
    statement = make_copy_command(table,infile)
    print(f"statement = [{statement}]")
    command = make_psql_command(statement,pgconf)
    print(f"command = {command}")
    outfile,errfile = logfiles(source,label)
    return command,outfile,errfile

def __exec_stage(pgconf,stage,source,label='current'):
    command,outfile,errfile = mkargs_stage(pgconf,stage,source)
    # load_args(pgconf,stage,source)
    log.info(f'command = {command}')
    print(f"letsgo = {command}")
    subprocess.Popen(
        ['nohup','time'] + command,
        stdout=open(outfile,'w'),
        stderr=open(errfile,'w'),
        preexec_fn=os.setpgrp)

def discover(stage,journal,source,version):
    print("locate (journal) ..")
    trunk = journal.locate_distinct(source)
    print(f"found {trunk}")
    for phase in trunk.phases():
        print(f"phase = {phase}")
        print(f"path  = {phase.path}")
        if version:
            subpath = phase.locate_distinct(version)
            print(f"version = {subpath}")
    print("locate (stage) ..")
    for issue in stage.locate(source,'csv'):
        print(f"found {issue}")


def main():
    args = parse_args()
    env = EnvironmentManager()
    print(env)
    print(tabulate(env.members()))
    # env.pgconf = slurp_json("config/postgres.json")
    log.info(f"stage = {env.stage}")
    log.info(f"source = {args.source}")
    print("let's go for a walk ..")
    source = args.source
    version = args.version
    discover(env.stage,env.journal,source,version)
    # exec_load(env.pgconf,env.stage,args.source)
    log.info("all done")

if __name__ == '__main__':
    main()










def __main():
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



"""
import os
import argparse
import subprocess
from collections import OrderedDict
import ioany
from ..util.io import slurp_json
from ..util.csvarg import make_csv_args
from ..logging import log
from kivo.environment.manager import EnvironmentManager

LOGDIR='log'
"""


def __make_psql_command(statement,pgconf):
    # quoted = '"'+statement+'"'
    hostname = pgconf.get('hostname')
    hostflag = " -h %s" % hostname if hostname else ''
    flags = "-U %(user)s -d %(dbname)s" % pgconf
    flags += hostflag
    flags = flags.split(" ")
    # command = "psql %s -c %s" % (flags,quoted)
    return ['psql'] + flags + ['-c'] + [statement]


def __make_copy_command(table,infile,char=','):
    csvargs = make_csv_args(char)
    return "\copy %s FROM %s %s;" % (table,infile,csvargs)

