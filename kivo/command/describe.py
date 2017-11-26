import os
from ..logging import log
from ..decorators import timedsingle
from .. import source
from .. import stage
from .util.execute import exec_source
from .. import module

HANDLERS = {}

def perform(posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    return exec_source(HANDLERS,posargs,options)

@timedsingle
def describe_module(modulename):
    log.debug('yo!')
    log.debug(f'modulename = {modulename}')
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


