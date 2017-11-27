from ..logging import log
from .util.misc import find_modules_under

INDEX = None

def build(path):
    log.debug('..')
    modules = list(find_modules_under(path))
    log.debug('that be %d modules' % len(modules))
    INDEX = ModuleIndex(modules)
    log.debug(f'index = {INDEX}')

class ModuleIndex(object):
    """
    An index to a base set of installed modules.
    So we can ask questions like "do any of our installed modules have config
    settings for a given tablespec (or prefix)"?
    """

    def __init__(self,modules):
        self.ingest(modules)

    def ingest(self,modules):
        for m in modules:
            self.add(m)

    def add(self,kivomod):
        pass

    def record(self,prefix,name):
        pass

