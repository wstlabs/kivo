import os
import glob
from .util.source import loadcfg_source
from .logging import log

MODPATH = "./modules"
SRCDIR = 'source'
CONFIG = {}

# Yes, this method doesn't seem to do much, at present.
# But it's a stub for an anticipated future change whereby the source directory 
# will be dynamically determined from the global install location.
def srcdir():
    """Return the path to the source configuration directory."""
    return SRCDIR

def configpath(prefix):
    return "%s/%s/source.yaml" % (MODPATH,prefix)

def loadcfg(prefix):
    path = configpath(prefix)
    log.debug(f'path = {path}')
    if not os.path.exists(path):
        raise ValueError("unrecognized source '%s'" % prefix)
    CONFIG[prefix] = loadcfg_source(path)
    return CONFIG[prefix]

def getcfg(prefix):
    config = CONFIG.get(prefix)
    return config if config else loadcfg(prefix)

def names(prefix):
    return sorted(getcfg(prefix).keys())

def getcfg_source(prefix,name,strict=True):
    """Shorthand to get the config dict for a named source.  If not present,
    a ValueError is raised."""
    log.debug(f'prefix.name = {prefix}.{name}')
    config = getcfg(prefix)
    tabcfg = config['tables']
    log.debug(f'tabcfg = {tabcfg}')
    if name in tabcfg:
        return tabcfg[name]
    if strict:
        raise ValueError("invalid source name '%s' for prefix '%s'" % (name,prefix))
    else:
        return None

def getval(prefix,name,attr,strict=True):
    """Shorthand to fetch an attribute value by source name.  The attribute need not
    be present, but the named source must be."""
    d = getcfg_source(prefix,name,strict)
    log.debug("config[%s] = %s" % (name,d))
    if strict and attr not in d:
        raise ValueError("invalid configuration - no '%s' attribute" % attr)
    return d.get(attr)


# In the future we may wish to allow the values in the query dict to be callables or regexes.
def matches(d,query):
    """
    Determines whether the given dict "matches" the given query.  At present this
    is taken to mean "have the same keys, and values match via the 'is' operator."
    """
    for k,v in query.items():
        if k not in d:
            return False
        if d[k] is not query[k]:
            return False
    return True

def select(prefix,query):
    """Given a source prefix, returns the names which match the given query
    (according to the match function in this module)."""
    config = getcfg(prefix)
    log.debug(f'config = {config}')
    tables = config['tables']
    return list(k for k,v in tables.items() if matches(v,query))


def exists(prefix,name=None):
    """Determines whether the named source (single or grouped) has a valid source configuration."""
    if prefix is None:
        raise ValueError("invalid usage -- need at least a prefix")
    config = getcfg(prefix)
    if config is None:
        return False
    if name is None:
        return True
    return name in config


#
# DEPRECATED
#

def __prefixes():
    """Returns, in sorted order, a list of prefixes for available data sources."""
    srcpat = "%s/*.yaml" % srcdir()
    files = (os.path.basename(_) for _ in glob.glob(srcpat))
    tuples = (os.path.splitext(_) for _ in files)
    return sorted((root for root,ext in tuples))


