import os
from collections import OrderedDict
from .core import Module

class ModuleIndex():

    def __init__(self,parent):
        self.parent = parent
        self._info = OrderedDict()
        self._miss = OrderedDict()
        self._done = False

    def __str__(self):
        return f"ModuleIndex({self.parent.path})"

    def add(self,name,info):
        if not isinstance(info,dict):
            raise ValueError("invalid info struct")
        assert_source_name(name)
        print(f"ADD name = {name} ..")
        if name in self._info:
            raise RuntimeError("conflict resolution not yet permitted")
        self._info[name] = info

    def get(self,name):
        return self._info.get(name)

    def build(self):
        if self._done:
            raise RuntimeError("invalid usage - already built")
        for module,sourcename in self.parent.sourcepairs():
            print(f"MODULE = {module}, sourcename = {sourcename}")
            info = module.source(sourcename)
            if info is None:
                raise ValueError(f"bad lookup on sourcename = '{sourcename}'")
            info['module'] = module.name
            self.add(sourcename,info)
        self._done = True

    def sources(self):
        yield from self._info.keys()



def assert_source_name(name):
    if not isinstance(name,str):
        raise ValueError("invalid source name")

