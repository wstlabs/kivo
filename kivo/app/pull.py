import re
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
    logbase=f"{source.name}--{version}--{pid}"
    if not os.path.exists(LOGDIR):
        os.mkdir(LOGDIR)
    outfile=f"{LOGDIR}/err--{logbase}.txt"
    errfile=f"{LOGDIR}/out--{logbase}.txt"
    return outfile,errfile

# target=f"https://data.cityofnewyork.us/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
def resolve(family,options):
    log.info(f"family = {family}, options = {options}")
    print(f"family = {family}, options = {options}")
    slug = options['slug']
    if family == 'socrata-newyork':
        return f"https://data.cityofnewyork.us/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
    if family == 'socrata-chicago':
        return f"https://data.cityofchicago.org/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
    if family == 'socrata-cookcounty':
        return f"https://datacatalog.cookcountyil.gov/api/views/{slug}/rows.csv?accessType=DOWNLOAD"
    raise ValueError(f"unknown source family '{family}'")

_slugpag = re.compile('^\w{4}-\w{4}$')
def is_valid_slug(slug):
    if not isinstance(slug,str):
        return False
    return _slugpat.match(slug)

def curlargs(journal,source,version):
    log.info(f"source = {source}, version = {version}")
    print(f'origin = {source.origin}')
    tempo = source.origin['tempo']
    phase = journal.trunk(tempo,source.name).phase(label='incoming',autoviv=True)
    destfile = phase.fullpath(f"{version}.csv")
    log.info(f"destfile = {destfile}")
    origin = source.origin
    target = resolve(origin['family'],origin['options'])
    log.info(f"target = {target}")
    command = ['curl','-o',destfile,target]
    outfile,errfile = logfiles(source,version)
    return command,outfile,errfile

def docurl(journal,source,version,dryrun=False):
    command,outfile,errfile = curlargs(journal,source,version)
    log.info(f'command = {command}')
    if dryrun:
        print('dryrun, aborting')
        return
    subprocess.Popen(
        ['nohup','time'] + command,
        stdout=open(outfile,'w'),
        stderr=open(errfile,'w'),
        preexec_fn=os.setpgrp)

def dopull(env,name,version):
    source = env.moduleindex.get(name)
    print(f"source = {source}")
    if source is None:
        raise ValueError(f"invalid sourcename '{name}'")
    docurl(env.journal,source,version,dryrun=False)

def main():
    args = parse_args()
    name = args.source
    version = args.version
    env = EnvironmentManager()
    print(env.dump())
    dopull(env,name,version)
    print("all done")


if __name__ == '__main__':
    main()




"""
def loadcfg(path):
    d = OrderedDict()
    inrecs = ioany.read_recs(path)
    for r in inrecs:
        slug,name = r['slug'],r['name']
        d[name] = {'slug':slug}
    return d
"""

def __curlargs(journal,slug,source,tempo,version):
    log.info(f"source = {source}, slug = {slug}")
    phase = journal.trunk(tempo,source).phase(label='incoming',autoviv=True)
    destfile = phase.fullpath(f"{version}.csv")
    log.info(f"destfile = {destfile}")
    target = resolve(tempo,slug)
    command = ['curl','-o',destfile,target]
    outfile,errfile = logfiles(source,version)
    return command,outfile,errfile

def __docurl(journal,slug,source,tempo,version):
    command,outfile,errfile = curlargs(journal,slug,source,tempo,version)
    log.info(f'command = {command}')
    subprocess.Popen(
        ['nohup','time'] + command,
        stdout=open(outfile,'w'),
        stderr=open(errfile,'w'),
        preexec_fn=os.setpgrp)

