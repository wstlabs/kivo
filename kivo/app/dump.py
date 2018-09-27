import os
import argparse
import subprocess
from collections import OrderedDict
import ioany
from ..logging import log
import kivo.fcache


LOGDIR='log'


def parse_args():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--source", type=str, required=True, help="source name")
    g.add_argument("--object", type=str, required=True, help="object name")
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

from ..util.csvarg import make_csv_args

"""
We use the '(select % from ...)' construct so that the relation we pull
from doesn't have to be table, as it would be if given as the direct argument
to the COPY command.  Introduces a very slight performance overhead, but is
vastly more flexible.
"""
def make_dump_command(table,outfile,char=','):
    csvargs = make_csv_args(char)
    return "\copy (select * from %s) TO %s %s;" % (table,outfile,csvargs)

