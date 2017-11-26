
class Module(object):

    def __init__(self,name,srccfg,pkgcfg=None):
        self._srccfg = srccfg
        self._pkgcfg = pkgcfg
        self.name = name

    def __str__(self):
        return f"Module(name='{self.name}')"

