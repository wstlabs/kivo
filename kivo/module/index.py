from ..logging import log

def build(path):
    pass

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

