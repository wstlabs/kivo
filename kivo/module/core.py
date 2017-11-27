from ..logging import log

class Module(object):

    def __init__(self,name,srccfg,pkgcfg=None):
        self._srccfg = srccfg
        self._pkgcfg = pkgcfg
        self.name = name

    def __str__(self):
        return f"Module(name='{self.name}')"

    def tables(self):
        for prefix,submap in self._srccfg['prefix'].items():
            # log.debug(f'prefix = {prefix}')
            for name in submap.keys():
                yield f'{prefix}.{name}'

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

