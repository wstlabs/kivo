import os
# from ...fcache.xdir import XDir
# from ...fcache.utils import is_dashy
from .core import Module

class ModuleIndex():

    def __init__(self,parent):
        self.parent = parent
        self.build()

    def __str__(self):
        return f"ModuleIndex({self.parent.path})"

    def build(self):
        pass

    def modules(self):
        pass
