import os
import kivo
from ..logging import log
from ..util.source import splitpath, tablename
from ..util.load import make_copy_command
from ..shell import dopsql
from ..decorators import timedsingle
from ..stage import theStage
from .util.execute import exec_other, exec_source

HANDLERS = {}

def perform(posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    return exec_source(HANDLERS,posargs,options)

@timedsingle
def load_tablespec(tablespec):
    prefix,name = split_table_spec(tablespec)
    log.debug(f'prefix = {prefix}, name = {name}')
    delta,status = load_source_canon(prefix,name)
    return status

@timedsingle
def load_prefix(prefix):
    raise NotImplementedError("not yet")

@timedsingle
def load_module(modulename):
    raise NotImplementedError("not yet")


HANDLERS = {
   'table':load_tablespec,
   'prefix':load_prefix,
   'module':load_module
}

@timedsingle
def load_source_canon(prefix,name):
    _stage = theStage
    log.debug(f'stage = {_stage}')
    log.debug(f'source = {prefix}.{name}')
    infile = _stage.latest(prefix,name)
    log.info("infile = '%s'" % infile)
    assert_loadable(prefix,name,infile)
    if not permit_loadable(prefix,name):
        raise ValueError("source inactive by configuration")
    table = tablename('t0',prefix,name)
    log.info("table = '%s'" % table)
    psql = make_copy_command(table,infile)
    log.debug("psql = [%s]" % psql)
    return dopsql(psql,kivo.pgconf)

def permit_loadable(prefix,name):
    """A simpe abstracted perms check which allows us to override config settings
    for certain special sources."""
    if prefix in ('temp','norm'):
        return True
    return source.getval(prefix,name,'active')

def assert_loadable(prefix,name,infile):
    if infile is None:
        raise RuntimeError("no loadable file for prefix = '%s', name ='%s'" % (prefix,name))
    if not os.path.exists(infile):
        raise RuntimeError("can't find infile '%s'" % infile)


#
# DEPRECATED
#

def __load_any(srcarg,strict=True):
    if '.' in srcarg:
        srcpath = srcarg
        prefix,name = splitpath(srcpath)
        return load_multi(prefix,[name],strict)
    else:
        prefix = srcarg
        names = source.select(prefix,{'active':True})
        return load_multi(prefix,names,strict)

def __load_multi(prefix,names,strict=True):
    """Load multiple named sourcs under a given prefix."""
    log.debug("names = %s" % names)
    for name in names:
        log.info("source %s.%s .." % (prefix,name))
        status,delta = load_source_named(prefix,name)
        _status = 'OK' if status else 'FAIL'
        log.info("source %s.%s - status = %s in %.3f sec" % (prefix,name,_status,delta))
        if strict and not status:
            return False
    return True

def __perform(posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    if len(posargs) == 1:
        return exec_source(load_source_named,posargs)
    else:
        raise ValueError("invalid usage")


