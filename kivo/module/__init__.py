import os
from ..logging import log
from .core import Module
from .util.misc import load_module_from, find_modules_under
from . import index

PATH = "./modules"
INDEX = None

def setup(path=PATH):
    log.debug('..')

def load(name,path=PATH):
    # modpath = "%s/%s" % (path,name)
    return load_module_from(path,name)

def find(dirpath=PATH):
    return find_modules_under(dirpath)

def info(prefix,name):
    return None

