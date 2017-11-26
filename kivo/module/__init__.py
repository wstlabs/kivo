import os
from .util.misc import load_module_from, find_modules_under

PATH = "./modules"

def load(name,path=PATH):
    modpath = "%s/%s" % (path,name)
    return load_module_from(modpath)

def find(dirpath=PATH):
    return find_modules_under(dirpath)

