import os
from ...fcache import XDir
from ...fcache.utils import is_valid_label
from ...util.mkdir import mkdir_from_base

class Module(XDir):

    def __init__(self,parent=None,name=None,autoviv=False):
        assert parent is not None
        assert name is not None
        self.parent = parent
        self._name = name
        self._package = None
        if autoviv:
            self.vivify()

    def __str__(self):
        return f"Module('{self._name}')"

    @property
    def subpath(self):
        return self._name

    @property
    def path(self):
        return self.parent.fullpath(self.subpath)

    def vivify(self):
        mkdir_from_base(self.parent.path,self.subpath)

    def inspect(self):
        if self.exists('package.json'):
            package = self.slurp_json('package.json')
            if not isinstance(package,dict):
                raise ValueError("invalid package struct")
            self._package = package
        else:
            raise ValueError("bad module structure - no package.json")

    @property
    def is_kosher(self):
        """
        Returns true of the module seems to have a coherent directory structure.
        """
        if not self.is_active:
            return False
        if self.exists('package.json'):
            return True
        return False

    def package(self,refresh=False):
        if self._package is None or refresh:
            self.inspect()
        return self._package

    @property
    def version(self,refresh=False):
        return self.package(refresh).get('version')

