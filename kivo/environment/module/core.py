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
        self.inspect()

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

    def inspect_package(self):
        self._package = None
        self._package_explain = None
        if self.exists('package.json'):
            package = self.slurp_json('package.json')
        else:
            self._package_explain = "cannot find package.json"
            return False
        if not isinstance(package,dict):
            self._package_explain = "invalid package struct"
            return False
        return True

    def inspect(self):
        self.inspect_package()

    @property
    def package(self):
        return self._package

    @property
    def version(self,refresh=False):
        if self.package is not None:
            return self.package.get('version')

    @property
    def is_kosher(self):
        """
        Returns true if the module seems to have a coherent directory structure.
        """
        if not self.is_active:
            return False
        if self.exists('package.json'):
            return True
        return False

