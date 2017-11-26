import re
from . import describe
from . import list_
from . import load
from . import pull
from . import dump
from . import check
from ..special import match

def command2module(command):
    """
    Returns the module name corresponding to a command name.  In most cases,
    the module name is exactly the command name, but in some cases it's slightly
    different (for example, as a hack to get around reserved word issues).
    """
    return 'list_' if command == 'list' else command

def resolve(command):
    """
    Given a (presumably valid) command name, attempts to resolve to the appropriate
    handler for the module corresponding to that command, and returns it.  If the module
    isn't loaded (or the command is syntactically invalid), returns None.
    """
    module = command2module(command)
    funcname = "%s.perform" % module
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

