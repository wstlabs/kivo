import os
import argparse
import subprocess
from collections import OrderedDict
import ioany
from ..logging import log
from kivo.environment.manager import EnvironmentManager


LOGDIR='log'

"""
time curl -o /opt/journal/monthly/acris-personal-legal/1-incoming/2018-09.csv \
     'https://data.cityofnewyork.us/api/views/uqqa-hym2/rows.csv?accessType=DOWNLOAD' >
          log/out-acris-personal-legal.log >& log/err-acris-personal-legal.log
"""


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

def logfiles(source,version):
    pid = os.getpid()
    logbase=f"{source}--{version}--{pid}"
    if not os.path.exists(LOGDIR):
        os.mkdir(LOGDIR)
    outfile=f"{LOGDIR}/err--{logbase}.txt"
    errfile=f"{LOGDIR}/out--{logbase}.txt"
    return outfile,errfile

# target=f"https://data.cityofnewyork.us/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
def resolve(tempo,slug):
    log.info(f"tempo = {tempo}, slug = {slug}")
    if tempo == 'socrata-newyork':
        return f"https://data.cityofnewyork.us/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
    if tempo == 'socrata-chicago':
        return f"https://data.cityofchicago.org/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
    raise ValueError(f"unknown tempo '{tempo}'")

def curlargs(journal,slug,source,tempo,version):
    log.info(f"source = {source}, slug = {slug}")
    phase = journal.trunk(tempo,source).phase(label='incoming',autoviv=True)
    destfile = phase.fullpath(f"{version}.csv")
    log.info(f"destfile = {destfile}")
    target = resolve(tempo,slug)
    command = ['curl','-o',destfile,target]
    outfile,errfile = logfiles(source,version)
    return command,outfile,errfile

def docurl(journal,slug,source,tempo,version):
    command,outfile,errfile = curlargs(journal,slug,source,tempo,version)
    log.info(f'command = {command}')
    subprocess.Popen(
        ['nohup','time'] + command,
        stdout=open(outfile,'w'),
        stderr=open(errfile,'w'),
        preexec_fn=os.setpgrp)

def loadcfg(path):
    d = OrderedDict()
    inrecs = ioany.read_recs(path)
    for r in inrecs:
        slug,name = r['slug'],r['name']
        d[name] = {'slug':slug}
    return d

def main():
    args = parse_args()
    source = args.source
    version = args.version
    env = EnvironmentManager()
    print("env = ",env)
    for line in env.members():
        print(line)
    # cfg = loadcfg("config/socrata.csv")
    # slug = cfg[source]['slug']
    info = env.moduleindex.get(source)
    print(f"info = {info}")
    tempo = 'monthly'
    log.info(f"source = {source}, tempo = {tempo}, version = {version}")
    docurl(env.journal,slug,source,tempo,version)
    log.info("all done")


if __name__ == '__main__':
    main()

