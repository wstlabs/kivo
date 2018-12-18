import os
from copy import deepcopy
from tabulate import tabulate
from .stage import Stage
from .journal import Journal
from .module.root import ModuleRoot
from .module.index import ModuleIndex
from ..config import resolve

_env = None
def default_instance():
    global _env
    if _env is None:
        _env = EnvironmentManager()
    return _env

class EnvironmentManager(object):

    def default():
        return default_instance()

    def __init__(self,**kwargs):
        self.build(**kwargs)

    def build(self,**kwargs):
        self._options = {}
        self._home = resolve('home')
        self.moduleroot = ModuleRoot()
        self.moduleindex = ModuleIndex(self.moduleroot)
        self.journal = Journal()
        self.stage   = Stage()

    @property
    def home(self):
        return self._home

    @property
    def logdir(self):
        return resolve('logdir')
        # return os.path.join(self.home,'log')

    @property
    def options(self):
        return deepcopy(self._options)

    def members(self):
        yield ('home',self.home)
        yield ('moduleroot',self.moduleroot)
        yield ('moduleindex',self.moduleindex)
        yield ('journal',self.journal)
        yield ('stage',self.stage)
        yield ('logdir',self.logdir)

    def dump(self):
        return tabulate(self.members())
