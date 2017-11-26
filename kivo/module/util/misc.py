import os

def load_module_from(path):
    if os.path.exists(path):
        config_source = config.source.load(path)
        return Module(config_source)
    else:
        return None

def find_modules_under(dirpath):
    yield 'foobar'

def is_module_dir(dirpath):
    """Return true if the pathname refers to an existing kivo module directory."""
    if not os.path.isdir(dirpath):
        return False
    srcpath = "%s/source.yaml" % dirpath
    return os.path.exists(srcpath)

