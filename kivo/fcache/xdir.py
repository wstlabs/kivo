import os
import ioany
# from ..logging import log

class XDir(object):

    def __init__(self,path,verify=False):
        self.setpath(path,verify)

    def __str__(self):
        return f"XDir({self.subpath})"

    @property
    def name(self):
        return str(type(self)).split('.')[-1]

    def setpath(self,path,verify=False):
        self._path = path
        if verify and not os.path.isdir(self._path):
            raise ValueError(f"can't verify path = {self._path}")

    @property
    def path(self):
        return self._path

    @property
    def is_active(self):
        return os.path.isdir(self.path)

    def assert_active(self):
        if not self.is_active:
            lcname = self.name.lower()
            raise RuntimeError(f"invalid usage - {lcname} inactive")

    def vivify(self):
        if not self.is_active:
            os.mkdir(self.path)

    def walk(self,**kwargs):
        top = self.path
        if os.path.isdir(top):
            return os.walk(top,**kwargs)
        else:
            raise RuntimeError("cannot traverse - path inactive")

    def getdirs(self):
        root,dirs,files = next(self.walk())
        return dirs

    def getfiles(self):
        root,dirs,files = next(self.walk())
        return files

    def getall(self):
        root,dirs,files = next(self.walk())
        return dirs + files

    def fullpath(self,subpath):
        assert subpath is not None
        return os.path.join(self.path,subpath)

    def exists(self,subpath):
        """
        Tests whether an object exists under the given path.
        Returns True for broken symbolic links.
        """
        path = self.fullpath(subpath)
        return os.path.lexists(path)

    def isdir(self,subpath):
        path = self.fullpath(subpath)
        return os.path.isdir(path)

    def isfile(self,subpath):
        path = self.fullpath(subpath)
        return os.path.isfile(path)

    def islink(self,subpath):
        path = self.fullpath(subpath)
        return os.path.islink(path)

    #
    # The next 3 methods are basically congruent (up to the slurp method).
    #

    def slurp_json(self,subpath,catch=True):
        path = self.fullpath(subpath)
        if not self.exists(path):
            raise ValueError(f"cannot find JSON file '{path}'")
        try:
            return ioany.slurp_json(path)
        except Exception as e:
            if catch:
                raise RuntimeError(f"bad JSON file '{path}'")
            else:
                raise e

    def slurp_yaml(self,subpath,catch=True):
        path = self.fullpath(subpath)
        if not self.exists(path):
            raise ValueError(f"cannot find YAML file '{path}'")
        try:
            return ioany.slurp_yaml(path)
        except Exception as e:
            if catch:
                raise RuntimeError(f"bad JSON file '{path}'")
            else:
                raise e

    def slurp_csv(self,subpath,catch=True):
        path = self.fullpath(subpath)
        if not self.exists(path):
            raise ValueError(f"cannot find CSV file '{path}'")
        try:
            return ioany.slurp_csv(path)
        except Exception as e:
            if catch:
                raise RuntimeError(f"bad CSV file '{path}'")
            else:
                raise e

