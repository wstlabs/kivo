import os
from collections import OrderedDict
from itertools import islice
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
        self._explain = OrderedDict()
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


    #
    # Inspection interface
    #

    def _disexplain(self,k):
        """
        Clears the explain status of the given tag from the internal _explain dict (if present).
        """
        if k in self._explain:
            del self._explain[k]

    def inspect_package(self):
        self._package = None
        self._disexplain('package')
        if self.exists('package.json'):
            package = self.slurp_json('package.json')
        else:
            self._explain['package'] = "no package.json"
            return False
        if not isinstance(package,dict):
            self._explain['package'] = "invalid package struct"
            return False
        self._package = package
        return True

    def inspect(self):
        self._explain = OrderedDict()
        self.inspect_package()

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

    @property
    def firsterror(self):
        """
        Returns the first error string (if any) from the most recent inspection attempt
        (or None if the inspection was successful).
        """
        top = _first(self._explain.keys())
        if len(top):
            k = top[0]
            return self._explain[k]

    #
    # Echo properties which (should have) emerged from our inspection operation.
    #

    @property
    def package(self):
        return self._package

    @property
    def version(self,refresh=False):
        if self.package is not None:
            return self.package.get('version')




def _first(iterable,depth=1):
    """
    A simple idiom to return the first :n items from an :iterable.  The iterable
    is expected to have at least that many items (otherwise, it allows a a StopIteration
    exception to bubble up).
    """
    return list(islice(iterable,depth))
