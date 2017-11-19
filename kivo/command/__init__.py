import re
from . import load
from . import pull
from . import dump
from . import check
from ..special import match


def resolve(command):
    """
    Given a (presumably valid) command name, attempts to resolve to the appropriate
    handler for the module corresponding to that command, and returns it.  If the module
    isn't loaded (or the command is syntactically invalid), returns None.
    """
    funcname = "%s.perform" % command
    if is_legit(command):
        try:
            handler = eval(funcname)
            return handler
        except Exception as e:
            pass
    return False

_pat = re.compile('^[_\w]+$')
def is_legit(command):
    return bool(re.match(_pat,command))

def nope():
    """
    if command == 'load':
        return load.perform
    if command == 'pull':
        return pull.perform
    if command == 'dump':
        return dump.perform
    if command == 'match':
        return match.perform
    return None
    """

