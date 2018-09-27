import os
from .issue import Issue
from ...fcache.xdir import XDir
from ...fcache.utils import is_dashy

ROOTDIR = '/opt/stage'

_stage = None
def instance():
    global _stage
    if _stage is None:
        _stage = Stage()
    return _stage


class Stage(XDir):

    def __init__(self,rootdir=ROOTDIR):
        self.setpath(rootdir,verify=True)

    def __str__(self):
        return f"Stage({self.path})"

    def issue(self,tag=None):
        if tag is None:
            raise ValueError("need an issue tag")
        assert is_dashy(tag)
        return Issue(self,tag)

    def resolve(self,tag,autoviv=True):
        """
        Similar to the 'issue' accessor in that it returns an Issue object for the
        given :tag, but provides special treatment for the 'current' :tag (which has
        certain constraints), and autovivifies by default (unless the :autoviv flag
        is provided and set to False).
        """
        issue = self.issue(tag)
        if tag == 'current':
            # if the 'current' alias is invoked, we require it to be a symbolic link (and already present as such). 
            if not issue.is_active:
                raise ValueError("the 'current' issue directory, unlike the others, cannot be auto-instantiated")
            if not issue.islink:
                raise ValueError("the 'current' issue needs to exist as a symbolic link, not an actual directory")
        else:
            # otherwise, we go ahead and autovivify.
            if autoviv and not issuedir.is_active:
                issue.vivify()
        return issue


"""
    def trunks(self):
        for family in valid_families():
            for source in self.sources(family):
                yield Trunk(self,family,source)

    def dive(self):
        for source in self.sources():
            yield source

    def locate(self,source):
        assert is_valid_source(source)
        for trunk in self.trunks():
            if trunk.source == source:
                yield trunk
"""

