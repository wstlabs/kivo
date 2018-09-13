import os
from .path import splitfull

def mkdir_from_base(basedir,subpath):
    if not os.path.isdir(basedir):
        raise ValueError(f"can't find basedir '{basedir}'")
    path = splitfull(subpath)
    curpath = basedir
    # print(f"subpath = {subpath}")
    for term in path:
        if '/' in term:
            raise ValueError(f"can't deal with path containing forward slash in term '{term}'")
        curpath = os.join(curpath,term):
        if not os.path.exists(curpath):
            os.mkdir(curpath)
    return curpath

