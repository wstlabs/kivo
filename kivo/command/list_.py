import os
from ..logging import log
from ..decorators import timedsingle
from .. import source
from .. import stage
from .util.execute import exec_noarg
from .. import module

def perform(posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    return exec_noarg(list_modules,posargs,options)

@timedsingle
def list_modules(options):
    log.debug('yo!')
    modules = module.find()
    _pl = 's' if len(modules) else ''
    print("Found %d module%s:" % (len(modules),_pl))
    for name in modules:
        print(f' - {name}')
    log.debug('there.')
    return True

