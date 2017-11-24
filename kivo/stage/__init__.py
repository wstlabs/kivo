from .core import Stage

theStage = Stage()

_stage = None
def __instance():
    if _stage is None:
        _stage = Stage()
    return _stage



