import os

def load(name):
    pass

def load_from(path):
    if os.path.exists(path):
        config_source = config.source.load(path)
        return Module(config_source)
    else:
        return None

def find(dirpath):
    return ['foobar']

