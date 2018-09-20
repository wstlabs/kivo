import os
from ..logging import log
from .core import Module
from .util.misc import load_module_from, find_modules_under
from . import index

# module path relative to the application root
# see init_app_root()
PATH = "modules"

def setup(path=PATH):
    log.debug('..')
    index.build(path)

def load(name,path=PATH):
    # modpath = "%s/%s" % (path,name)
    return load_module_from(path,name)

def find(dirpath=PATH):
    return find_modules_under(dirpath)

def info(prefix,name):
    return None

