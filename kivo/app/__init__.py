import re
from . import bind
from . import dump
from . import env
from . import find
from . import liszt
from . import load
from . import pull
from . import throw
# from . import describe
# from . import refresh
# from . import check
# from . import truncate

def command2app(command):
    """
    Returns the module name corresponding to a command name.  In most cases,
    the module name is exactly the command name, but in some cases it's slightly
    different (for example, we hack 'list' to 'liszt' to get around reserved
    word issues).
    """
    return 'liszt' if command == 'list' else command

def resolve(command):
    """
    Given a (presumably valid) command name, attempts to resolve to the appropriate
    handler for the module corresponding to that command, and returns it.  If the module
    isn't loaded (or the command is syntactically invalid), returns None.
    """
    module = command2app(command)
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

