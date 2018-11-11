import os
from ...fcache import XDir
from ...fcache.utils import phasetup
from ...fcache.utils import valid_labels
from ...fcache.utils import is_valid_tempo
from ...fcache.utils import is_valid_source
from ...util.mkdir import mkdir_from_base
from .phase import Phase

class Trunk(XDir):

    def __init__(self,parent,tempo,source):
        self.build(parent,tempo,source)

    def build(self,parent,tempo,source):
        # assert isinstance(parent,Journal)
        assert is_valid_tempo(tempo)
        assert is_valid_source(source)
        self.parent = parent
        self.tempo = tempo
        self.source = source

    def __str__(self):
        return f"Trunk({self.subpath})"

    @property
    def subpath(self):
        return os.path.join(self.tempo,self.source)

    @property
    def path(self):
        rootdir = self.parent.path
        subpath = self.subpath
        return os.path.join(rootdir,subpath)

    def vivify(self):
        journal = self.parent
        journal.assert_active()
        mkdir_from_base(journal.path,self.subpath)

    def phase(self,index=None,label=None,autoviv=False):
        index,label = phasetup(index,label)
        return Phase(self,label,autoviv)

    def phases(self):
        for label in valid_labels():
            phase = self.phase(label=label)
            if os.path.isdir(phase.path):
                yield phase


