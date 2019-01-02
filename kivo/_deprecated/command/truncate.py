import os
import kivo
from ..logging import log
from ..shell import dopsql
from ..decorators import timedsingle

def perform(posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    return truncate_table(posargs[0])

@timedsingle
def truncate_table(name):
    log.info(f'name = {name}')
    psql = make_truncate_command(name)
    log.debug("psql = [%s]" % psql)
    return dopsql(psql,kivo.pgconf)

def make_truncate_command(table,concurrent=True):
        return f'truncate table {table};'

