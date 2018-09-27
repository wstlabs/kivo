import os
from ...fcache import XDir
from ...fcache.utils import is_valid_label
from ...util.mkdir import mkdir_from_base

class Issue(XDir):

    def __init__(self,parent=None,tag=None,autoviv=False):
        assert parent is not None
        assert tag is not None
        self.parent = parent
        self.tag = tag
        if autoviv:
            self.vivify()

    def __str__(self):
        return f"Issue('{self.tag}')"

    @property
    def subpath(self):
        return self.tag

    @property
    def path(self):
        return self.parent.fullpath(self.subpath)

    def vivify(self):
        mkdir_from_base(self.parent.path,self.subpath)
