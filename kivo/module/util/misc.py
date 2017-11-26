import os
from .core import Module
from . import config

PATH = "./modules"

def load(name):
    pass

def load_from(path):
    if os.path.exists(path):
        config_source = config.source.load(path)
        return Module(config_source)
    else:
        return None

def find(dirpath=PATH):
    return ['foobar']

