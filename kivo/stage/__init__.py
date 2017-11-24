from .core import Stage

_stage = None
def instance():
    if _stage is None:
        _stage = Stage()
    return _stage



