import os
from ..logging import log
from ..decorators import timedsingle
from .. import source
from .. import stage
from .util.execute import exec_noarg
from .. import module

def perform(posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    return exec_noarg(describe_source,posargs,options)

@timedsingle
def describe_source(options):
    log.debug('yo!')
    log.debug('there.')
    return True

