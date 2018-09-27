from .environment.manager import EnvironmentManager

_env = None
def stdenv():
    if _env is None:
        _env = EnvironmentManager()
    return env



