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
    parser.add_argument("--issue", type=str, required=True, default="current", help="issue tag")
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

def __mkargs_bind(pgconf,stage,source,label='current'):
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

def __exec_bind(pgconf,stage,source,label='current'):
    command,outfile,errfile = mkargs_stage(pgconf,stage,source)
    # load_args(pgconf,stage,source)
    log.info(f'command = {command}')
    print(f"letsgo = {command}")
    subprocess.Popen(
        ['nohup','time'] + command,
        stdout=open(outfile,'w'),
        stderr=open(errfile,'w'),
        preexec_fn=os.setpgrp)

# BindStatPre = namedtuple('BindStatPre',['phase','subpath','issue','error'])
def discover(stage,journal,source,version,issuetag):
    print("locate (journal) ..")
    trunk = journal.locate_distinct(source)
    if trunk is None:
        print(f"trunk not found!")
        return False
    print(f"trunk = {trunk}")
    for phase in trunk.phases():
        print(f"phase = {phase}")
        print(f"path  = {phase.path}")
        if version:
            subpath = phase.locate_distinct(version)
            print(f"version = {subpath}")
    print("locate (stage) ..")
    for issue in stage.locate(source,'csv'):
        print(f"found {issue}")

def perform(stage,journal,sourcename,version,issuetag):
    print("now ...")
    phase,subpath,error = journal.discover(sourcename,version)
    print(f"phase = {phase}")
    print(f"subpath = {subpath}")
    print(f"error = {error}")
    status = stage.presents(issuetag,sourcename,ext='csv')
    print(f"status = {status}")

def main():
    args = parse_args()
    env = EnvironmentManager()
    print(env)
    print(tabulate(env.members()))
    # env.pgconf = slurp_json("config/postgres.json")
    log.info(f"stage = {env.stage}")
    log.info(f"source = {args.source}")
    if args.more:
        print(":: discover ..")
        discover(env.stage,env.journal,args.source,args.version,issuetag=args.issue)
    print(":: perform ..")
    perform(env.stage,env.journal,args.source,args.version,issuetag=args.issue)
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


