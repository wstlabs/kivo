import os
from .core import Module
from .util.misc import load_module_from, find_modules_under

PATH = "./modules"
INDEX = None

def build_index(path):
    pass

def load(name,path=PATH):
    # modpath = "%s/%s" % (path,name)
    return load_module_from(path,name)

def find(dirpath=PATH):
    return find_modules_under(dirpath)

def info(prefix,name):
    return None

