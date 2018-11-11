import os
from ...fcache.xdir import XDir
from ...fcache.utils import phasedir
from ...fcache.utils import label2index
from ...fcache.utils import is_valid_label
from ...fcache.utils import is_valid_version
from ...util.mkdir import mkdir_from_base

class Phase(XDir):

    def __init__(self,parent=None,label=None,autoviv=False):
        assert parent is not None
        assert is_valid_label(label)
        self.parent = parent
        self.label = label
        if autoviv:
            self.vivify()

    def __str__(self):
        tempo  = self.parent.tempo
        source = self.parent.source
        label  = self.label
        return f"Phase('{tempo}','{source}','{label}')"

    def index(self):
        return label2index(self.label)

    @property
    def subpath(self):
        return phasedir(label=self.label)

    @property
    def path(self):
        trunkdir = self.parent.path
        return os.path.join(trunkdir,self.subpath)

    def vivify(self):
        self.parent.vivify()
        mkdir_from_base(self.parent.path,self.subpath)

    def locate(self,version):
        assert is_valid_version(version)
        for fname in self.getall():
            root,ext = os.path.splitext(fname)
            if root == version:
                yield fname

    def locate_distinct(self,version):
        matches = list(self.locate(version))
        n = len(matches)
        if n == 0:
            return None
        if n == 1:
            return matches[0]
        raise ValueError("too many matches for version = '{version}'")

