import os
from ...fcache.xdir import XDir
from ...fcache.utils import is_dashy
from .core import Module

ROOTDIR = '/opt/build/kivo/modules'

_root = None
def instance():
    global _root
    if _root is None:
        _root = ModuleRoot()
    return _root

class ModuleRoot(XDir):

    def __init__(self,rootdir=ROOTDIR):
        self.setpath(rootdir,verify=True)

    def __str__(self):
        return f"ModuleRoot({self.path})"

    def module(self,name=None,verify=True):
        if name is None:
            raise ValueError("need a module name")
        assert is_dashy(name)
        module = Module(self,name)
        if verify:
            if not module.is_active:
                raise ValueError(f"can't find module '{module}'")
        return module

    def modules(self):
        dirs = self.getdirs()
        # print(f"DIRS = {dirs}")
        for name in self.getdirs():
            if not is_dashy(name):
                continue
            # print(f"NAME = {name} ..")
            module = self.module(name)
            if module.is_active:
                yield module

    def sourcepairs(self):
        for module in self.modules():
            if module.is_sourced:
                for sourcename in module.sources():
                    yield module,sourcename


