import os
from collections import OrderedDict
from .logging import log

ROOTDIR = '/opt/stage'
PHASERANK = OrderedDict([('special',4),('xtracted',3),('unpack',2),('incoming',1),('proto',0)])

class Stage(object):

    def __init__(self,rootdir=None):
        if rootdir is None:
            rootdir = ROOTDIR
        self.rootdir = rootdir


    def dirpath(self,phase,prefix):
        j = PHASERANK.get(phase)
        phasedir = "%d-%s" % (j,phase) if j is not None else phase
        return "%s/%s/%s" % (self.rootdir,phasedir,prefix)

    def filepath(self,phase,prefix,name):
        _dirpath = self.dirpath(phase,prefix)
        return "%s/%s.csv" % (_dirpath,name)

    def mkdir_phase(self,phase,prefix,autoviv=False):
        _dirpath = self.dirpath(phase,prefix)
        if not os.path.exists(_dirpath):
            if autoviv:
                os.mkdir(_dirpath)
            else:
                raise ValueError("invalid state -- can't find dirpath '%s'" % _dirpath)
        return _dirpath

    def mkpath(self,phase,prefix,name,autoviv=False):
        _dirpath = self.mkdir_phase(phase,prefix,autoviv)
        return "%s/%s.csv" % (_dirpath,name)

    def latest(self,prefix,name):
        for phase in PHASERANK.keys():
            _filepath = self.filepath(phase,prefix,name)
            # print("%s.%s:%s -> %s" % (prefix,name,phase,_filepath))
            if os.path.exists(_filepath):
                return _filepath
        return None


"""
def export(prefix,name,stage=STAGE,autoviv=False):
    return mkpath(stage,'export',prefix,name,autoviv)

def incoming(prefix,name,stage=STAGE,autoviv=False):
    return mkpath(stage,'incoming',prefix,name,autoviv)
"""


