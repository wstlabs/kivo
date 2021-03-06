import os
from ..logging import log
from ..decorators import timedsingle
from .util.execute import exec_source
from .. import stage
from .. import module

HANDLERS = {}

def perform(posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    return exec_source(HANDLERS,posargs,options)

@timedsingle
def describe_module(modulename):
    log.debug('yo!')
    log.debug(f'modulename = {modulename}')
    kivomod = module.load(modulename)
    log.info(f'kivomod = {kivomod}')
    tables = list(kivomod.tables())
    n = len(tables)
    _pl = '' if n == 1 else 's'
    log.info(f'with {n} table{_pl}:')
    for table in tables:
        log.info(f' - {table}')
    log.debug('happy')
    return True

@timedsingle
def describe_tablespec(tablespec):
    log.debug('yo!')
    log.debug(f'tablespec = {tablespec}')
    return True

HANDLERS = {
    'module':describe_module,
    'table':describe_tablespec
}


