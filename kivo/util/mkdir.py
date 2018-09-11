import os
from .path import splitfull

def mkdir_from_base(basedir,path):
    if not os.path.isdir(basedir):
        raise ValueError(f"can't find basedir '{basedir}'")
    path = splitfull(path)
    curpath = basedir
    print(f"path = {path}")
    for term in path:
        if '/' in term:
            raise ValueError(f"can't deal with path terms containing forward slash in term '{term}'")
        curpath = f"{curpath}/{term}"
        if not os.path.exists(curpath):
            os.mkdir(curpath)
    return curpath

