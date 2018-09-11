import os
import argparse
import subprocess
from collections import OrderedDict
import ioany
from ..logging import log
from ..util.mkdir import mkdir_from_base


ROOT='/opt/journal'
LOGDIR='log'

"""
time curl -o /opt/journal/monthly/acris-personal-legal/1-incoming/2018-09.csv \
     'https://data.cityofnewyork.us/api/views/uqqa-hym2/rows.csv?accessType=DOWNLOAD' >
          log/out-acris-personal-legal.log >& log/err-acris-personal-legal.log
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, help="source name")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--month", type=str, required=False, help="monthly version tag")
    g.add_argument("--year", type=str, required=False, help="yearly version tag")
    args = parser.parse_args()
    if args.month is not None:
        args.family = 'monthly'
        args.version = args.month
    if args.year is not None:
        args.family = 'yearly'
        args.version = args.year
    return args

def make_dest_dir(family,name):
    if not os.path.exists(ROOT):
        assert RuntimeError("can't find journal root '{ROOT}', aborting")
    subpath = f"{family}/{name}/1-incoming"
    destdir = mkdir_from_base(ROOT,subpath)
    return destdir

def logfiles(name,version):
    pid = os.getpid()
    logbase=f"{name}--{version}--{pid}"
    if not os.path.exists(LOGDIR):
        mkdir(LOGDIR)
    outfile=f"{LOGDIR}/err--{logbase}.txt"
    errfile=f"{LOGDIR}/out--{logbase}.txt"
    return outfile,errfile

def curlargs(slug,name,family,version):
    destdir = make_dest_dir(family,name)
    destfile = f"{destdir}/{version}.csv"
    log.info(f"destfile = {destfile}")
    target=f"https://data.cityofnewyork.us/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
    command = ['curl','-o',destfile,target]
    outfile,errfile = logfiles(name,version)
    return command,outfile,errfile

def execcurl(slug,name,family,version):
    command,outfile,errfile = curlargs(slug,name,family,version)
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
    name = args.name
    version = args.version
    cfg = loadcfg("config/socrata.csv")
    slug = cfg[name]['slug']
    family = 'monthly'
    log.info(f"name = {name}, family = {family}, version = {version}")
    execcurl(slug,name,family,version)
    log.info("all done")


if __name__ == '__main__':
    main()

