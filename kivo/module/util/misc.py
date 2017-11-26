import os

def load_module_from(path):
    if os.path.exists(path):
        config_source = config.source.load(path)
        return Module(config_source)
    else:
        return None

def find_modules_under(dirpath):
    yield 'foobar'

