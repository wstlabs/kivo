import os
import kivo
from ..logging import log
from ..util.refresh import make_refresh_command
from ..shell import dopsql
from ..decorators import timedsingle
from .util.execute import exec_other, exec_source

HANDLERS = {}

def perform(posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    return refresh_matview(posargs[0])

@timedsingle
def refresh_matview(name):
    log.info(f'name = {name}')
    psql = make_refresh_command(name)
    log.debug("psql = [%s]" % psql)
    return dopsql(psql,kivo.pgconf)

def assert_loadable(tablename,infile):
    if infile is None:
        raise RuntimeError("no loadable file for tablename ='%s'" % (tablename))
    if not os.path.exists(infile):
        raise RuntimeError("can't find infile '%s'" % infile)

