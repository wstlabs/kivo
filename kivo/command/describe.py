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
def describe_module(options):
    log.debug('yo!')
    return True

@timedsingle
def describe_table(options):
    log.debug('yo!')
    return True

HANDLERS = {
    'module':describe_module,
    'table':describe_table
}


