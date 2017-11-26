import os
from ...logging import log

def load_module_from(path):
    if os.path.exists(path):
        config_source = config.source.load(path)
        return Module(config_source)
    else:
        return None

def find_modules_under(basedir):
    if not os.path.isdir(basedir):
        raise ValueError("invalid module directory path (not a directory)")
    subdirs = os.scandir(basedir)
    module_names = list(_.name for _ in subdirs)
    # log.debug('hey')
    # for name in module_names:
    #    log.debug(f'name = {name}')
    return (name for name in module_names if is_module_dir(f'{basedir}/{name}'))


def is_module_dir(dirpath):
    """Return true if the pathname refers to an existing kivo module directory."""
    log.debug(f'is dirpath={dirpath}?')
    if not os.path.isdir(dirpath):
        return False
    srcpath = "%s/source.yaml" % dirpath
    return os.path.exists(srcpath)

