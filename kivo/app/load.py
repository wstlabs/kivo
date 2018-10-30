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
time curl -o /opt/journal/monthly/acris-personal-legal/1-incoming/2018-09.csv \
     'https://data.cityofnewyork.us/api/views/uqqa-hym2/rows.csv?accessType=DOWNLOAD' >
          log/out-acris-personal-legal.log >& log/err-acris-personal-legal.log
"""

def make_copy_command(table,infile,char=','):
    csvargs = make_csv_args(char)
    return "\copy %s FROM %s %s;" % (table,infile,csvargs)

def make_psql_command(statement,pgconf):
    # quoted = '"'+statement+'"'
    hostname = pgconf.get('hostname')
    hostflag = " -h %s" % hostname if hostname else ''
    flags = "-U %(user)s -d %(dbname)s" % pgconf
    flags += hostflag
    flags = flags.split(" ")
    # command = "psql %s -c %s" % (flags,quoted)
    return ['psql'] + flags + ['-c'] + [statement]

def source2table(source,schema='t0'):
    table = source.replace('-','_')
    return f"{schema}.{table}"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, required=True, help="source name")
    parser.add_argument("--dry", action="store_true")
    return parser.parse_args()

def logfiles(source,version):
    pid = os.getpid()
    logbase=f"{source}--{version}--{pid}"
    if not os.path.exists(LOGDIR):
        os.mkdir(LOGDIR)
    outfile=f"{LOGDIR}/err--{logbase}.txt"
    errfile=f"{LOGDIR}/out--{logbase}.txt"
    return outfile,errfile

def load_args(pgconf,stage,source,label='current'):
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
    # target=f"https://data.cityofnewyork.us/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
    # command = ['curl','-o',destfile,target]
    outfile,errfile = logfiles(source,label)
    return command,outfile,errfile

def exec_load(pgconf,stage,source):
    command,outfile,errfile = load_args(pgconf,stage,source)
    # load_args(pgconf,stage,source)
    log.info(f'command = {command}')
    print(f"letsgo = {command}")
    subprocess.Popen(
        ['nohup','time'] + command,
        stdout=open(outfile,'w'),
        stderr=open(errfile,'w'),
        preexec_fn=os.setpgrp)


def main():
    args = parse_args()
    env = EnvironmentManager()
    env.pgconf = slurp_json("config/postgres.json")
    log.info(f"stage = {env.stage}")
    log.info(f"source = {args.source}")
    exec_load(env.pgconf,env.stage,args.source)
    log.info("all done")


if __name__ == '__main__':
    main()

