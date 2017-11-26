import os
from .core import Module
from .config import loadcfg_source

PATHS = ["./modules"]

def load(name):
    pass

def load_from(path):
    if os.path.exists(path):
        config = loadcfg_source(path)
        return Module(config)
    else:
        return None

