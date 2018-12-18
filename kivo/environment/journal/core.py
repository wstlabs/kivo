import os
from .trunk import Trunk
from ...fcache.xdir import XDir
from ...fcache.utils import valid_tempos, is_dashy, is_valid_tempo, is_valid_source

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

    def temporoot(self,tempo):
        assert is_valid_tempo(tempo)
        return os.path.join(self.path,tempo)

    def sources(self,tempo):
        temporoot = self.temporoot(tempo)
        if os.path.isdir(temporoot):
            for name in os.listdir(temporoot):
                if is_dashy(name):
                    yield name
        else:
            yield from []

    def trunk(self,tempo=None,source=None):
        if tempo is None:
            raise ValueError("need a tempo name")
        if source is None:
            raise ValueError("need a source name")
        return Trunk(self,tempo,source)

    def trunks(self):
        for tempo in valid_tempos():
            for source in self.sources(tempo):
                yield Trunk(self,tempo,source)

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

    def discover(self,sourcename,version):
        assert is_dashy(sourcename)
        assert is_dashy(version)
        trunk = self.locate_distinct(sourcename)
        if trunk is None:
            return None,None,"trunk not found"
        latest,target = None,None
        for phase in trunk.phases():
            subpath = phase.locate_distinct(version)
            if subpath is not None:
                latest,target = phase,subpath
        return latest,target,None

