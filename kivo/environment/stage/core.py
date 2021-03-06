import os
from .issue import Issue
from ...fcache.xdir import XDir
from ...fcache.utils import is_dashy, is_ext

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

    def issues(self):
        dirpath,subdirs,files = next(self.walk())
        for tag in subdirs:
            yield Issue(self,tag)

    def locate(self,source,ext='csv'):
        assert is_dashy(source)
        assert is_ext(ext)
        for issue in self.issues():
            if issue.presents(source,ext):
                yield issue

    def presents(self,issuetag,source,ext):
        issue = self.issue(issuetag)
        return None if issue is None else issue.presents(source,ext)

