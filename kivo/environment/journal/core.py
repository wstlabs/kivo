import os
from .trunk import Trunk
from ...fcache.xdir import XDir
from ...fcache.utils import valid_families, is_dashy, is_valid_family, is_valid_source

ROOTDIR = '/opt/journal'

_journal = None
def instance():
    global _journal
    if _journal is None:
        _journal = Journal()
    return _journal


class Journal(XDir):

    def __init__(self,rootdir=ROOTDIR):
        self.setpath(rootdir,verify=True)

    def __str__(self):
        return f"Journal({self.path})"

    def famdir(self,family):
        assert is_valid_family(family)
        return os.path.join(self.path,family)

    def sources(self,family):
        famdir = self.famdir(family)
        if os.path.isdir(famdir):
            for name in os.listdir(famdir):
                if is_dashy(name):
                    yield name
        else:
            yield from []

    def trunk(self,family=None,source=None):
        if family is None:
            raise ValueError("need a family name")
        if source is None:
            raise ValueError("need a source name")
        return Trunk(self,family,source)

    def trunks(self):
        for family in valid_families():
            for source in self.sources(family):
                yield Trunk(self,family,source)

    def dive(self):
        for source in self.sources():
            yield source

    def locate(self,source):
        assert is_valid_source(source)
        for trunk in self.trunks():
            if trunk.source == source:
                yield trunk

    def locate_distinct(self,source):
        trunks = list(self.locate(source))
        n = len(trunks)
        if n == 0:
            return None
        if n == 1:
            return trunks[0]
        raise RuntimeError(f"multiple trunks for source = '{source}'")

