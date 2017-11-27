from ...logging import log
from ...util.source import splitpath, tablename
from ...decorators import timedsingle

def extract_source(options):
    """Extract source argument (and type) from options struct."""
    # In theory, both of the failure cases (both options present, or neither present) 
    # has already been excluded via the 'add_mutually_exclusive_group' construct in parse_args().  
    # But to be really robust we need to check explicitly at this stage, as well.
    if options.module and options.table:
        raise ValueError("invalid usage (--module and --table options are mutuallly exclusive)")
    if options.module:
        return {'module':options.module}
    if options.table:
        return {'table':options.table}
    raise ValueError("invalid usage (exactly one of the --module or--table must be present)")

def exec_noarg(handler,posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    if len(posargs):
        raise ValueError("invalid usage (too many positional arguments)")
    status,delta = handler(options)
    _status = 'OK' if status else 'FAIL'
    log.info("<noarg> - status = %s in %.3f sec" % (_status,delta))
    return status

def exec_source(handlers,posargs=None,options=None):
    log.debug("posargs=%s, options=%s" % (posargs,options))
    if len(posargs):
        raise ValueError("invalid usage (too many positional arguments)")
    source = extract_source(options)
    return _exec_source(handlers,source)

def _exec_source(handlers,source):
    module = source.get('module')
    tablespec  = source.get('table')
    if module is not None:
        handler = handlers.get('module')
        return _exec_module(handler,module)
    if tablespec is not None:
        handler = handlers.get('table')
        return _exec_tablespec(handler,tablespec)
    # This case really shouldn't happen if our logic in extract_source() is correct. 
    raise RuntimeError("invalid state")

def exec_other(handler,posargs=None,options=None):
    status,delta = handler(posargs)
    _status = 'OK' if status else 'FAIL'
    log.info("status = %s in %.3f sec" % (_status,delta))
    return status

def _exec_module(handler,module):
    log.debug(f'module = {module}')
    log.info(f'module = {module} ..')
    status,delta = handler(module)
    _status = 'OK' if status else 'FAIL'
    log.info("module %s - status = %s in %.3f sec" % (module,_status,delta))
    return status

def _exec_tablespec(handler,tablespec):
    log.debug(f'tablespec = {tablespec}')
    raise RuntimeError("not finished")
    if '.' in tablespec:
        srcpath = tablespec
        log.debug(f'srcpath = {srcpath}')
        raise RuntimeError("not finished")
        # prefix,name = splitpath(srcpath)
        # log.debug(f'name = {name}')
        # return exec_src_multi(handler,prefix,[name])
    else:
        prefix = srcarg
        raise RuntimeError("not finished")
        # log.debug(f'prefix = {prefix}')
        # names = source.select(prefix,{'active':True})
        # log.debug(f'names = {names}')
        # return exec_src_multi(handler,prefix,names)

def exec_src_multi(handler,prefix,names):
    """Do something for multiple named sources under a given prefix."""
    log.debug(f'names = {names}')
    for name in names:
        log.info("source %s.%s .." % (prefix,name))
        status,delta = handler(prefix,name)
        _status = 'OK' if status else 'FAIL'
        log.info("source %s.%s - status = %s in %.3f sec" % (prefix,name,_status,delta))
        if not status:
            return False
    return True

def uniqarg(posargs):
    if posargs is not None:
        if len(posargs) == 0:
            return None
        if len(posargs) == 1:
            return posargs[0]
    raise ValueError("invalid usage (too many positional arguments)")

