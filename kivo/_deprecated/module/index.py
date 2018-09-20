from copy import deepcopy
from collections import OrderedDict
from ..logging import log
from .util.misc import find_modules_under, load_module_from

INDEX = None

def build(path):
    global INDEX
    log.debug('..')
    names = list(find_modules_under(path))
    log.debug('that be %d modules' % len(names))
    modules = (load_module_from(path,name) for name in names)
    INDEX = ModuleIndex(modules)
    log.debug(f'index = {INDEX}')
    log.debug('index len = %d' % len(INDEX))
    for t in INDEX.tables():
        m = INDEX.resolve(*t)
        r = INDEX.lookup(*t)
        # log.debug(f'table = {t} => {m.name} => {r}')
    log.debug(f'finally: index = {INDEX}')

def lookup(prefix,name):
    global INDEX
    # log.debug(f'{prefix}.{name}')
    # log.debug(f'index = {INDEX}')
    if INDEX is None:
        raise RuntimeError("invalid usage - module index not initialized")
    return INDEX.lookup(prefix,name)


class ModuleIndex(object):
    """
    An index to a base set of installed modules.
    So we can ask questions like "do any of our installed modules have config
    settings for a given tablespec (or prefix)"?
    """

    def __init__(self,modules):
        self.count = 0
        self._map = OrderedDict()
        self.ingest(modules)

    def __len__(self):
        return self.count

    def ingest(self,modules):
        for m in modules:
            log.debug(f'm = {m}')
            self.add(m)
            self.count += 1

    def add(self,kivomod):
        log.debug(f'kivomod = {kivomod}')
        for prefix,name in kivomod.tables():
            if prefix not in self._map:
                self._map[prefix] = OrderedDict()
            if name in self._map[prefix]:
                raise ValueError("duplicate tablespec {prefix}.{name} detected")
            self._map[prefix][name] = kivomod

    def resolve(self,prefix,name):
        d = self._map.get(prefix)
        if d is not None:
            return d.get(name)

    def lookup(self,prefix,name):
        # log.debug(f'{prefix}.{name}')
        m = self.resolve(prefix,name)
        if m is not None:
            return m.info(prefix,name)

    def tables(self):
        for prefix,submap in self._map.items():
            for name in submap.keys():
                yield prefix,name


