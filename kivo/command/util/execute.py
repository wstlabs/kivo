from ...logging import log
from ...util.source import splitpath, tablename
from ...decorators import timedsingle
from ... import source

def exec_other(handler,posargs=None,options=None):
    status,delta = handler(posargs)
    _status = 'OK' if status else 'FAIL'
    log.info("status = %s in %.3f sec" % (_status,delta))
    return status

def exec_src(handler,posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    srcarg = uniqarg(posargs)
    return exec_src_any(handler,srcarg)

def exec_src_any(handler,srcarg,strict=True):
    if '.' in srcarg:
        srcpath = srcarg
        prefix,name = splitpath(srcpath)
        return exec_src_multi(handler,prefix,[name],strict)
    else:
        prefix = srcarg
        names = source.select(prefix,{'active':True})
        return exec_src_multi(handler,prefix,names,strict)

def exec_src_multi(handler,prefix,names,strict=True):
    """Do something for multiple named sources under a given prefix."""
    log.debug("names = %s" % names)
    for name in names:
        log.info("source %s.%s .." % (prefix,name))
        status,delta = handler(prefix,name)
        _status = 'OK' if status else 'FAIL'
        log.info("source %s.%s - status = %s in %.3f sec" % (prefix,name,_status,delta))
        if strict and not status:
            return False
    return True

def uniqarg(posargs):
    if posargs is not None:
        if len(posargs) == 0:
            return None
        if len(posargs) == 1:
            return posargs[0]
    raise ValueError("invalid usage (too many positional arguments)")

