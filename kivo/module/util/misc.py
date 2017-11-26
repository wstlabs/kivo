import os
import re
from ...logging import log
from .. import config
from ...module import Module

def load_module_from(path,name):
    log.debug(f'path = {path}, name = {name} ..')
    modpath = "%s/%s" % (path,name)
    if os.path.exists(modpath):
        srccfg = config.source.load(modpath)
        log.debug(f'srccfg = {srccfg}')
        return Module(name,srccfg)
    else:
        return None

def find_modules_under(basedir):
    """Returns a geneator which yields a sequence of (apparently) valid kivo modules under the given basedir."""
    if not os.path.isdir(basedir):
        raise ValueError("invalid module directory path (not a directory)")
    subdirs = os.scandir(basedir)
    module_names_possible = (_.name for _ in subdirs)
    module_names_valid = (_ for _ in module_names_possible if is_module_name(_))
    return (name for name in module_names_valid if is_module_dir(f'{basedir}/{name}'))
    # module_names_valid = list(_ for _ in module_names_possible if is_module_name(_))
    # log.debug('hey')
    # for name in module_names:
    #    log.debug(f'name = {name}')


def is_module_dir(dirpath):
    """Return true if the pathname refers to an existing kivo module directory."""
    # log.debug(f'is dirpath={dirpath}?')
    if not os.path.isdir(dirpath):
        return False
    srcpath = "%s/source.yaml" % dirpath
    return os.path.exists(srcpath)

_pat = re.compile('^([A-Z0-9]+-)*([A-Z0-9]+)$',re.IGNORECASE)
def is_module_name(name):
    """Returns true if the given string is a structurally valid module name."""
    return re.match(_pat,name)

