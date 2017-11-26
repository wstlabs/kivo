import os
from ..logging import log
from ..decorators import timedsingle
from .. import source
from .. import stage
from .util.execute import exec_other, exec_source

def perform(posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    path = uniqarg(posargs)
    return exec_any(check_source_named,path)

@timedsingle
def check_source_named(prefix,name):
    log.debug("source = '%s'.'%s'" % (prefix,name))
    infile = stage.latest(prefix,name)
    return infile is not None

