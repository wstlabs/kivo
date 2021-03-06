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
                yield prefix,name

    def info(self,prefix,name):
        d = self._srccfg['prefix'].get(prefix)
        # log.debug(f'prefix = {prefix} => {d}')
        # log.debug(f'srccfg = {self._srccfg}')
        if d is not None:
            return d.get(name)
