import os
import argparse
import subprocess
from collections import OrderedDict
import ioany
from ..logging import log
import kivo.fcache


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
        args.family = 'monthly'
        args.version = args.month
    if args.year is not None:
        args.family = 'yearly'
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

def curlargs(journal,slug,source,family,version):
    phase = journal.trunk(family,source).phase(label='incoming',autoviv=True)
    destfile = phase.fullpath(f"{version}.csv")
    log.info(f"destfile = {destfile}")
    target=f"https://data.cityofnewyork.us/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
    command = ['curl','-o',destfile,target]
    outfile,errfile = logfiles(source,version)
    return command,outfile,errfile

def docurl(journal,slug,source,family,version):
    command,outfile,errfile = curlargs(journal,slug,source,family,version)
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
    cfg = loadcfg("config/socrata.csv")
    slug = cfg[source]['slug']
    family = 'monthly'
    log.info(f"source = {source}, family = {family}, version = {version}")
    journal = kivo.fcache.journal.instance()
    docurl(journal,slug,source,family,version)
    log.info("all done")


if __name__ == '__main__':
    main()

